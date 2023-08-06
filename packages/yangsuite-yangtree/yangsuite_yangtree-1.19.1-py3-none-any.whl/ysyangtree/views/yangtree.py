import os
import warnings
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ysyangtree.context import reset_parse_yang, YSContext
from ysyangtree.ymodels import YSYangModels, DEFAULT_INCLUDED_NODETYPES
from yangsuite.logs import get_logger
from ysfilemanager import split_user_set, YSYangSet
from django.utils.html import escape

log = get_logger(__name__)
rfc_info_cache = {}


NODETYPE_TO_RFC_SECTION = {
    'anyxml': '7.10',
    'case': '7.9.2',
    'choice': '7.9',
    'container': '7.5',
    'grouping': '7.11',
    'identity': '7.16',
    'input': '7.13.2',
    'leaf': '7.6',
    'leaf-list': '7.7',
    'leafref': '9.9',
    'list': '7.8',
    'notification': '7.14',
    'output': '7.13.3',
    'rpc': '7.13',
    'typedef': '7.3',
}


@login_required
def get_rfc(request):
    """Get the Json object with RFC content of each nodetype.

    Parse the RFC content if not cached, else return cached information.
    """
    nodetype = request.POST.get('nodetype')

    if not nodetype:
        return JsonResponse({'content': 'module'})

    if nodetype not in rfc_info_cache and nodetype in NODETYPE_TO_RFC_SECTION:
        rfc_info_cache[nodetype] = rfc_section_text(
            NODETYPE_TO_RFC_SECTION[nodetype])

    if rfc_info_cache.get(nodetype, None):
        return JsonResponse({
            'content': rfc_info_cache[nodetype],
            'reference': ("https://tools.ietf.org/html/rfc6020#section-" +
                          NODETYPE_TO_RFC_SECTION[nodetype]),
        })
    else:
        log.info("No specific page range known for nodetype '%s'", nodetype)
        return JsonResponse({'content': 'No additional information known',
                             'reference': ''})


def rfc_section_text(start, end=None):
    """Function to retrieve the requested subsection of RFC 6020."""
    with open(os.path.join(os.path.dirname(__file__), 'rfc6020.txt')) as fd:
        content = fd.read().splitlines()
    if not end:
        subs = start.split(".")
        subs[-1] = str(int(subs[-1]) + 1)
        end = ".".join(subs)
    for i, line in enumerate(content):
        if line.startswith(start):
            content = content[i:]
            break
    else:
        # we finished the loop without finding a match
        log.error("Did not find start section '%s' in the RFC.", start)
        return ""

    for i, line in enumerate(content):
        if line.startswith(end):
            content = content[:i]
            break
    else:
        log.warning("Did not find end section '%s' in the RFC.", end)

    return escape("\n".join(content))


##########################################
# Django view functions below this point #
##########################################


def ctx_status(ref, yangset=None):
    """Report the status of the context associated with the given key."""
    ctx = YSContext.get_instance(ref, yangset)
    if ctx is None:
        return JsonResponse({}, status=404,
                            reason="No request in progress.")
    return JsonResponse({
        'value': ctx.load_status['count'],
        'max': ctx.load_status['total'],
        'info': ctx.load_status['info'],
    })


@login_required
def get_tree(request):
    """Retrieve context and build the JSTree based on module name.

    Args:
      request (django.http.HttpRequest): HTTP POST request

        - ref (str): reference for finding shared context (default: username)
        - name (str): module name to be parsed (DEPRECATED)
        - names (list): module name(s) to parse
        - yangset (str): YANG set name 'owner:setname' to use with context.
        - included_nodetypes (list): nodetypes to include in the tree.
          If unspecified, defaults to
          :const:`ymodels.DEFAULT_INCLUDED_NODETYPES`.
    Returns:
      django.http.JsonResponse: JSTree
    """
    if request.method == 'POST':
        names = request.POST.getlist('names[]')
        if not names:
            name = request.POST.get('name')
            if name:
                warnings.warn('Please provide a list "names[]" instead of '
                              'a single "name" parameter.', DeprecationWarning)
                names = [name]

        if not names:
            return JsonResponse({}, status=400,
                                reason="No model name(s) specified")

        yangset = request.POST.get('yangset')
        try:
            owner, setname = split_user_set(yangset)
        except ValueError:
            return JsonResponse({}, status=400,
                                reason="Invalid yangset string")
        try:
            ys = YSYangSet.load(owner, setname)
        except (OSError, ValueError):
            return JsonResponse({}, status=404, reason="No such yangset")

        ref = request.POST.get('reference')
        if not ref:
            ref = request.user.username

        included_nodetypes = request.POST.getlist('included_nodetypes[]',
                                                  DEFAULT_INCLUDED_NODETYPES)

        # Do we have a cached instance already?
        models = YSYangModels.get_instance(ref)
        if ((not models) or
                models.modelnames != sorted(names) or
                models.ctx.repository != ys or
                models.ctx.repository.is_stale):
            # Not a valid cache entry - need a new one
            try:
                ctx = YSContext.get_instance(ref, yangset)
            except RuntimeError:
                return JsonResponse({}, status=404, reason="No such user")
            except KeyError:
                return JsonResponse({},
                                    status=404,
                                    reason='Bad cache reference')
            if ctx is None:
                return JsonResponse({}, status=404,
                                    reason="User context not found")
            models = YSYangModels(ctx, names,
                                  included_nodetypes=included_nodetypes)
        else:
            models.included_nodetypes = included_nodetypes
        # Stay backwards compatible - [get|reset]_parse_yang expects a
        # single ParseYang instance, not a YSYangModels instance.
        reset_parse_yang(models.yangs[names[0]], ref)
        # Store the YSYangModels with the new class API
        YSYangModels.store_instance(models, ref)

        return JsonResponse(models.jstree)
    else:
        yangset = request.GET.get('yangset')
        ref = request.GET.get('reference')
        if not ref:
            ref = request.user.username
        return ctx_status(ref, yangset)


@login_required
def explore(request, yangset=None, modulenames=None):
    """Render the base yangtree explore page, with optional selections.

    Args:
      request (django.http.HttpRequest): HTTP GET request

        -  yangset (str): YANG set slug 'owner+setname' to auto-select.
        -  modulenames (str): module name(s) to auto-select from this yangset,
           as comma-separated list of the form "module-1,module-2,module-3"
    Returns:
      django.http.HttpResponse: page to display
    """
    return render(request, 'ysyangtree/yangtree.html', {
        'yangset': yangset or '',
        'modulenames': modulenames or '',
    })
