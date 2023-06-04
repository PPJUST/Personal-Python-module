# 自用的sqlite3库的简单封装

import sqlite3

class SQLiteDB:
    def __init__(self, db_file):
        # 打开数据库连接
        self.conn = sqlite3.connect(db_file)
        # 获取游标
        self.cur = self.conn.cursor()

    def create_table(self, table_name, column_datatype:dict, primary_key=None):
        """创建数据表
        输入变量：
        table_name：表格名称
        column_datatype：列名与数据类型对应的字典
        primary_key：主键，可选参数
        """
        # 将输入的参数转换为sqlite语句支持的样式
        sql_convert = ', '.join([i + ' ' + column_datatype[i] for i in column_datatype])
        if primary_key not is None and primary_key in column_datatype:
          sql_column.replace(f'{primary_key} {column_datatype[primary_key]}', f'{primary_key} {column_datatype[primary_key]} Primary KEY')
        # 创建数据表，如果不存在则创建
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({sql_convert})"
        self.cur.execute(sql)
        # 提交执行结果到数据库
        self.conn.commit()

    def add_record(self, table_name, column_value:dict):
        """插入数据
        输入变量：
        table_name：表格名称
        column_value：列名与对应列的数据的字典
        """
        # 将输入的参数转换为sqlite语句支持的样式
        sql_column = ', '.join([i for i in column_value])
        sql_value = ', '.join([column_value[i] for i in column_value])
        # 新增记录
        sql = f"INSERT INTO {table_name}({sql_column}) VALUES ({sql_value})"
        self.cur.execute(sql)
        # 提交执行结果到数据库
        self.conn.commit()

    def update_record(self, table_name, column, value, condition):
        """更新数据
        输入变量：
        table_name：表格名称
        column：列名
        value：列对应的值
        condition：条件，可使用 AND 或 OR
        """
        # 更新记录
        sql = f"UPDATE {table_name} SET {column} = '{value}' WHERE {condition}"
        self.cur.execute(sql)
        # 提交执行结果到数据库
        self.conn.commit()

    def delete_record(self, table_name, condition):
       """删除数据
        输入变量：
        table_name：表格名称
        condition：条件，可使用 AND 或 OR
        """
        # 删除记录
        sql = f"DELETE FROM {table_name} WHERE {condition}"
        self.cur.execute(sql)
        # 提交执行结果到数据库
        self.conn.commit()

    def get_record(self, table_name, column='*':list, condition=None):
        """查询数据
        输入变量：
        table_name：表格名称
        column：需要查询的列名列表
        condition：条件，可使用 AND 或 OR
        """
        if condition is None:
          if column == '*':
            sql = f'SELECT * FROM {table_name}'
           elif type(column) is str:
            sql = f'SELECT {column} FROM {table_name}'
           elif type(column) is list:
            sql = f'SELECT {', '.join(column)} FROM {table_name}'
        elif condition not is None:
          if column == '*':
            sql = f'SELECT * FROM {table_name} WHERE {condition}'
           elif type(column) is str:
            sql = f'SELECT {column} FROM {table_name} WHERE {condition}'
           elif type(column) is list:
            sql = f'SELECT {', '.join(column)} FROM {table_name} WHERE {condition}'
        self.cur.execute(sql)
        # 获取对应记录
        return self.cur.fetchall()
      
      def create_new_column(self, table_name, column_datatype:dict):
        """插入新的列
        输入变量：
        table_name：表格名称
        column_datatype：列名与数据类型对应的字典
        """
        # 将输入的参数转换为sqlite语句支持的样式
        sql_convert = ', '.join([i + ' ' + column_datatype[i] for i in column_datatype])

        # 插入新列
        sql = f"ALTER TABLE {table_name} ADD COLUMN {sql_convert}"
        self.cur.execute(sql)
        # 提交执行结果到数据库
        self.conn.commit()
      
      
      def copy_table(self, old_table_name , new_table_name):
        """复制数据表
        输入变量：
        old_table_name：需要复制的表格名称
        new_table_name：新的表格名称
        """
        # 复制表格结构
        sql_frame = f"CREATE TABLE {new_table_name} AS SELECT * FROM {old_table_name} WHERE 0"
        self.cur.execute(sql_frame)
        # 复制表格数据
        sql_record = f"INSERT INTO {new_table_name} SELECT * FROM {old_table_name}"
        self.cur.execute(sql_record)
        # 提交执行结果到数据库
        self.conn.commit()
      
      
      def is_exist(self, table_name):
        """数据库中是否存在指定数据表
        输入变量：
        table_name：表格名称
        """
        # 查询数据表是否存在
        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        self.cur.execute(sql)
        if cursor.fetchone() is not None:
          return True
        else:
            return False
        
        def show_all_table(self)
        """输出数据库中的所有数据表"""
        sql = f"SELECT name FROM sqlite_master WHERE type='table'"
        self.cur.execute(sql)
        return cursor.fetchone()
      
      

    def close(self):
        # 关闭数据库连接
        self.conn.close()
