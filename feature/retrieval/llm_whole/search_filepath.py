import os

# def total_file_path():
#     # 設定根目錄路徑（相對路徑）
#     directory_path = r".\餐廳評論爬蟲 (1)"  # 使用相對路徑

#     # 初始化一個清單來儲存店名
#     store_names = []

#     # 遍歷目錄中的所有檔案
#     for root, dirs, files in os.walk(directory_path):
#         for file in files:
#             if file.endswith(".json"):  # 僅處理 .json 檔案
#                 # 提取店名（去掉文件擴展名 .json）
#                 store_name = os.path.splitext(file)[0]
#                 store_names.append(store_name)



#     return store_names

# if __name__ == "__main__":
#         # 列印找到的店名
#     for name in total_file_path():
#         print(name)



def total_file_path(directory_path):
    # 設定根目錄路徑（相對路徑）
    directory_path = directory_path  # r".\餐廳評論爬蟲 (1)"  # 使用相對路徑

    # 初始化一個清單來儲存店名
    store_names = []

    # 遍歷目錄中的所有檔案
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".json"):  # 僅處理 .json 檔案
                # 提取店名（去掉文件擴展名 .json）
                store_name = os.path.splitext(file)[0]
                store_names.append(store_name)



    return store_names

if __name__ == "__main__":
        # 列印找到的店名
    # for name in total_file_path(r".\餐廳評論爬蟲 (1)"):
    #     print(name)

    # for name in total_file_path('embeding_data'):
    #     print(name)

    print(total_file_path('embeding_data'))