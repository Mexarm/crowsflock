
import re

from functools import partial

ATTACHMENT_SETUP_PATTERN = re.compile(r'\<(FIELD|SECRET)\:(.+?)\>')


def traverse_dict(dic, key_list):
    ''' returns the final value after traversing the dict with the key_list'''
    ret = dic
    for key in key_list:
        ret = ret[key]
    return ret

# render('    sasasa   dsds<FIELD:first_name>.....<SECRET:mysecret001>',
#         dict(FIELD=pd, SECRET=secrets))


def render(template, pattern, context):
    ret = template[:]
    traverse_partial = partial(traverse_dict, context)

    def func(matchobj):
        return traverse_partial(matchobj.groups(0))

    return re.sub(pattern, func, ret)

 # render_attachment_setup('    sasasa   dsds<FIELD:first_name>.....<SECRET:mysecret001>',
 # dict(FIELD=pd, SECRET=secrets))


def render_attachment_setup_pattern(template, context):
    return render(template, ATTACHMENT_SETUP_PATTERN, context)


# auth_json = render.render_attachment_setup_pattern(json.dumps(aa.setup['auth']),
# dict(SECRET=Secret.get_all_as_dict(t)))

# json.loads(auth_json)
