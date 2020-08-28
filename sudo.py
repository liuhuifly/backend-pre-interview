import time

class SuDoHandler:

    def __init__(self):
        self.data_list = []
        self.sum_data_list = []
        self.input_file = 'sudoku.txt'
        self.output_file = 'sudoku_solution.txt'
        with open(self.input_file, mode='r', encoding='utf8') as of:
            lines = of.readlines()
            for i in range(0, len(lines), 10):
                item = [[0 for s_i in range(9)] for s_j in range(9)]
                for j in range(9):
                    index = i + j + 1
                    line = lines[index].strip('\n')
                    if len(line) == 9:
                        for s_j in range(9):
                            item[j][s_j] = int(line[s_j])

                self.data_list.append(item)    
        
    def data_init(self, data):
        self.finish_flag = False
        self.current_data = data
        self.current_available_data = [[[v for v in range(1, 10)] for s_i in range(9)] for s_j in range(9)]
        self.current_sum_first_three_numbers = 0

        for row_index in range(9):
            for col_index in range(9):
                cell_value = self.current_data[row_index][col_index]
                if cell_value != 0:
                    self.current_available_data[row_index][col_index] = []
                    item_row_base_index = row_index // 3
                    item_col_base_index = col_index // 3
                    for index in range(9):
                        item_row_index = (item_row_base_index * 3) + (index // 3)
                        item_col_index = (item_col_base_index * 3) + (index % 3)

                        if self.current_data[row_index][index] == 0 and cell_value in self.current_available_data[row_index][index]:
                            self.current_available_data[row_index][index].remove(cell_value)
                        elif self.current_data[index][col_index] == 0 and cell_value in self.current_available_data[index][col_index]:
                            self.current_available_data[index][col_index].remove(cell_value)
                        elif self.current_data[item_row_index][item_col_index] == 0 and cell_value in self.current_available_data[item_row_index][item_col_index]:
                            self.current_available_data[item_row_index][item_col_index].remove(cell_value)

        for row_index in range(9):
            for col_index in range(9):
                if len(self.current_available_data[row_index][col_index]) == 1:
                    self.current_data[row_index][col_index] = self.current_available_data[row_index][col_index][0]
    
    def sum_first_three_numbers(self):
        for col_index in range(3):
            self.current_sum_first_three_numbers += self.current_data[0][col_index]
        self.sum_data_list.append(self.current_sum_first_three_numbers)

    def back_track(self, row_index:int, col_index:int):
        if row_index == 8 and col_index >= 9:
            self.finish_flag = True
            return
        
        if col_index == 9:
            row_index += 1
            col_index = 0
        
        if self.current_data[row_index][col_index] == 0:
            available_values = self.current_available_data[row_index][col_index]
            for cell_value in available_values:
                if self.bound(row_index, col_index, cell_value):
                    self.current_data[row_index][col_index] = cell_value
                    self.back_track(row_index, col_index + 1)
                    if self.finish_flag == False:
                        self.current_data[row_index][col_index] = 0
            
        else:
            self.back_track(row_index, col_index + 1)

    def bound(self, row_index:int, col_index:int, cell_value:int) -> bool:
        item_row_index = row_index // 3
        item_col_index = col_index // 3

        for index in range(9):
            if self.current_data[row_index][index] == cell_value:
                return False
            elif self.current_data[index][col_index] == cell_value:
                return False
            elif self.current_data[(item_row_index * 3) + (index // 3)][(item_col_index * 3) + (index % 3)] == cell_value:
                return False
        return True

    def data_print(self):
        for row in range(9):
            line = ''
            for col in range(9):
                line += str(self.current_data[row][col])

                if col < 8:
                    line += ('|' if ((col + 1) % 3) == 0 else ' ')

            print(line)
            if (row != 8) and ((row + 1) % 3) == 0:
                print('-' * 17)
    
    def data_output(self):
        with open(self.output_file, mode='w', encoding='utf8') as of:
            index = 1
            for data in self.data_list:
                line = 'Grid ' + str(index)
                of.write(line + '\n')
                
                for row in range(9):
                    line = ''
                    for col in range(9):
                        line += str(data[row][col])
                    of.write(line + '\n')
                index += 1

if __name__ == "__main__":
    
    handler = SuDoHandler()
    
    if len(handler.data_list) > 0:
        index = 0
        for item in handler.data_list:
            index += 1
            handler.data_init(item)

            print(f'# question {index}')
            handler.data_print()
            handler.back_track(0, 0)
            handler.sum_first_three_numbers()

            print('\n')
            print(f'# solution {index}')
            
            handler.data_print()
            print('\n')
            print(f'# sum of first three numbers: {handler.current_sum_first_three_numbers}')
            print('\n')
        
        handler.data_output()
        sum_list = sum(handler.sum_data_list)
        print(f'# sum for each of the {len(handler.sum_data_list)} puzzles: {sum_list}')
