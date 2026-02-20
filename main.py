variables = {}

def execute(code):
    code = code.replace(";", " ; ").replace("=", " = ").replace("+", " + ")
    tokens = code.split()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == "var":
            var_name = tokens[i + 1]
            value = tokens[i + 3]
            
            if value.isdigit():
                variables[var_name] = int(value)
            else:
                variables[var_name] = value
            
            i += 4

        elif token == "print":
            var_name = tokens[i + 1]
            result = variables.get(var_name, "Error: Variable not found")
            print("Vertex output:", result)
            i += 2

        elif i + 1 < len(tokens) and tokens[i + 1] == "=":
            target = token
            op1 = tokens[i + 2]
            
            if i + 3 < len(tokens) and tokens[i + 3] == "+":
                op2 = tokens[i + 4]
                
                if op1.isdigit():
                    val1 = int(op1)
                else:
                    val1 = variables.get(op1, 0)
                
                if op2.isdigit():
                    val2 = int(op2)
                else:
                    val2 = variables.get(op2, 0)
                
                variables[target] = val1 + val2
                i += 5
            else:
                i += 1
        else:
            i += 1

if __name__ == "__main__":
    example_code = """
    var age = 15 ;
    var bonus = 5 ;
    total = age + bonus ;
    print total ;
    """
    execute(example_code)