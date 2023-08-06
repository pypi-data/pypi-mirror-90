import mysql.connector
import logging


class MySqlClient:
    """Client to deal with MySQL database interactions. Besides the usual db data,
     need to provide table name where the information of the posts are as well as the name
     of the columns for the post image path and the caption text. The table used for the posts
     should have a column named 'posted'. It would be a boolean to keep track of the posts have
     already been posted on IG"""
    def __init__(self, host: str, username: str, password: str, database: str, table: str, img_path_column: str,
                 caption_txt_column: str):
        self.table = table
        self.img_path_col = img_path_column
        self.caption_txt_col = caption_txt_column
        try:
            self.db = mysql.connector.connect(
                host=host,
                user=username,
                password=password,
                database=database
            )
        except mysql.connector.Error as e:
            logging.error("Error while connecting to DB: " + format(e))
            raise

    def get_posts_data(self):
        """Gets the posts that are pending to be posted ('posted' column => false)"""
        try:
            cur = self.db.cursor()
            cur.execute(
                "SELECT id, " + self.img_path_col + ", " + self.caption_txt_col + " FROM " + self.table + " WHERE posted = false")
            result = cur.fetchall()
            return result
        except mysql.connector.Error as e:
            logging.error("Error while retrieving data from DB: " + format(e))
            return None

    def get_one_post_data(self):
        """Gets the posts that are pending to be posted ('posted' column => false)"""
        try:
            cur = self.db.cursor()
            cur.execute(
                "SELECT id, " + self.img_path_col + ", " + self.caption_txt_col + " FROM " + self.table + " WHERE posted = false LIMIT 1")
            result = cur.fetchall()
            return result
        except mysql.connector.Error as e:
            logging.error("Error while retrieving data from DB: " + format(e))
            return None

    def update_to_posted(self, post_id: int):
        """Updates to posted the corresponding post ('posted' column => true)"""
        try:
            cur = self.db.cursor()
            cur.execute("UPDATE " + self.table + " SET posted = true WHERE id = " + str(post_id))
            self.db.commit()
        except mysql.connector.Error as e:
            logging.error("Error while updating post data in DB: " + format(e))
            raise
