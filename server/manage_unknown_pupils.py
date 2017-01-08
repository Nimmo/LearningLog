import class_management as class_manager


if __name__ == "__main__":
    class_list = class_manager.load_class_list()
    class_manager.manage_pupils(class_list)
