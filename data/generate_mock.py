import os

def generate_mock_java():
    base_dir = "mock_project"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # 1. The God Object
    print("Generating God Object...")
    with open(os.path.join(base_dir, "SystemGod.java"), "w") as f:
        f.write("public class SystemGod {\n")
        f.write("    public void init() {\n")
        f.write("        ManagerA ma = new ManagerA();\n")
        f.write("        ma.doWork();\n")
        f.write("        ManagerB mb = new ManagerB();\n")
        f.write("        mb.doMoreWork();\n")
        f.write("    }\n")
        # Add 500 methods to make it a true God object
        for i in range(500):
            f.write(f"    public void handleEverything{i}() {{\n")
            f.write(f"        // doing everything {i}\n")
            f.write(f"        Util u = new Util();\n")
            f.write(f"        u.helper{i % 50}();\n")
            f.write("    }\n")
        # Add a dead path
        f.write("    public void unusedGodMethod() {\n")
        f.write("        // never called\n")
        f.write("    }\n")
        f.write("}\n")

    # 2. Spaghetti Managers (Cyclical dependencies)
    print("Generating Spaghetti Managers...")
    with open(os.path.join(base_dir, "ManagerA.java"), "w") as f:
        f.write("public class ManagerA {\n")
        f.write("    public void doWork() {\n")
        f.write("        ManagerB mb = new ManagerB();\n")
        f.write("        mb.callbackA();\n")
        for i in range(100):
            f.write(f"        // dummy logic {i}\n")
        f.write("    }\n")
        f.write("    public void callbackB() {\n")
        f.write("        // End cycle\n")
        f.write("    }\n")
        f.write("}\n")

    with open(os.path.join(base_dir, "ManagerB.java"), "w") as f:
        f.write("public class ManagerB {\n")
        f.write("    public void doMoreWork() {\n")
        f.write("        // independent logic\n")
        f.write("    }\n")
        f.write("    public void callbackA() {\n")
        f.write("        ManagerA ma = new ManagerA();\n")
        f.write("        ma.callbackB();\n")
        f.write("    }\n")
        f.write("}\n")

    # 3. Utilities (Many methods to bulk up line count)
    print("Generating Utilities...")
    with open(os.path.join(base_dir, "Util.java"), "w") as f:
        f.write("public class Util {\n")
        for i in range(100):
            f.write(f"    public void helper{i}() {{\n")
            f.write(f"        System.out.println(\"Helper {i}\");\n")
            for j in range(20):
                f.write(f"        // bulk line {j}\n")
            f.write("    }\n")
        f.write("}\n")

    # 4. Dead Code Classes (Ghost code)
    print("Generating Dead Code Classes...")
    with open(os.path.join(base_dir, "OldFeature.java"), "w") as f:
        f.write("public class OldFeature {\n")
        f.write("    public void deprecatedMethod() {\n")
        f.write("        // Never called from SystemGod or anywhere reachable\n")
        f.write("    }\n")
        f.write("}\n")
        
    # Bulk Generator
    print("Generating Bulk Classes...")
    for class_id in range(50):
        with open(os.path.join(base_dir, f"Service{class_id}.java"), "w") as f:
            f.write(f"public class Service{class_id} {{\n")
            f.write("    public void start() {\n")
            if class_id < 49:
                f.write(f"        Service{class_id+1} s = new Service{class_id+1}();\n")
                f.write("        s.start();\n")
            f.write("    }\n")
            for m in range(20):
                f.write(f"    public void internal{m}() {{\n")
                for line in range(10):
                    f.write(f"        int x = {line};\n")
                f.write("    }\n")
            f.write("}\n")
            
    print("Done!")

if __name__ == '__main__':
    generate_mock_java()
