# from importlib import import_module

# base = "models"
# modules = [
#     {"module": "user", "class": "User"},
#     {"module": "post", "class": "Post"},
# ]

# for item in modules:
#     globals()[item['class']] = getattr(import_module(
#         base + '.' + item['module']), item['class'])
