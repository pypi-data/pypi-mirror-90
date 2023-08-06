import logging


def validate_args(geckodriver_path,
                  username,
                  password,
                  kwargs,
                  validate_kwargs: bool):
    if geckodriver_path is None:
        logging.error("Must provide a geckodriver path")
        return False
    if username is None:
        logging.error("Must provide a username")
        return False
    if password is None:
        logging.error("Must provide a password")
        return False
    if validate_kwargs:
        if kwargs.get('mysql_host') is None:
            logging.error("Must provide a db host 'mysql_host'")
            return False
        if kwargs.get('mysql_username') is None:
            logging.error("Must provide a db username 'mysql_username'")
            return False
        if kwargs.get('mysql_password') is None:
            logging.error("Must provide a db password 'mysql_password'")
            return False
        if kwargs.get('mysql_database') is None:
            logging.error("Must provide a database name 'mysql_database'")
            return False
        if kwargs.get('mysql_posts_table') is None:
            logging.error("Must provide a posts table name 'mysql_posts_table'")
            return False
        if kwargs.get('mysql_img_path_column') is None:
            logging.error("Must provide the column name for the posts image paths 'mysql_img_path_column'")
            return False
        if kwargs.get('mysql_img_path_column') is None:
            logging.error("Must provide the column name where the posts caption text are 'mysql_caption_txt_column'")
            return False
    return True
