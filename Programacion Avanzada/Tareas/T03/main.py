from user_interact import load_function, main_menu

if __name__ == "__main__":
    graph = load_function()
    main_menu(graph[0].value, graph[1].value, graph[2].value, graph[3].value,
              graph[4].value)
