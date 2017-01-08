import class_management


if __name__ == "__main__":
    class_list = class_management.load_class_list()
    class_management.manage_pupils(class_list)