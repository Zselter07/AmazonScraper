# allowed_extensions is an array, like ['jpg', 'jpeg', 'png']
class ImagePaths:

    def file_paths_from_folder(self, root_folder_path, allowed_extensions=['jpg', 'png'], recursive=True):
        import os

        root_folder_path = os.path.abspath(root_folder_path)
        file_paths = []

        for (dir_path, _, file_names) in os.walk(root_folder_path):
            abs_dir_path = os.path.abspath(dir_path)

            for file_name in file_names:
                if allowed_extensions is not None and len(allowed_extensions) > 0:
                    for extension in allowed_extensions:
                        if file_name.lower().endswith(extension.lower()):
                            file_paths.append(os.path.join(abs_dir_path, file_name))

                            break
                else:
                    file_paths.append(os.path.join(abs_dir_path, file_name))
            
            if not recursive:
                break
        
        return file_paths