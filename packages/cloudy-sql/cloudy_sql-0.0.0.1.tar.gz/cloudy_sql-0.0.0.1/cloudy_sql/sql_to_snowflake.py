from cloudy_sql.snowflake_objects.snowflake_object import SnowflakeObject
from IPython.core.magic import (Magics, magics_class, cell_magic)

# SQL Writer Object
@magics_class
class SQLWriter(SnowflakeObject, Magics):

    @cell_magic
    def sql_to_snowflake(self, cell):
        try:
            # configure and connect to Snowflake
            self.initialize_snowflake()

            self.cursor = self.connection.cursor()

            query_results = self.cursor.execute(cell)

        # catch and log error
        except Exception as e:
            self.log_message = e
            self._logger.error(self.log_message)
            return False

        finally:
            # close connection and cursor
            if self.connection:
                self.connection.close()
            if self.cursor:
                self.cursor.close()

        # log successful clone
        self.log_message = f"Successfully ran SQL query in Snowflake"
        self._logger.info(self.log_message)
        return query_results
