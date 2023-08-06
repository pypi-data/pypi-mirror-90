import sys,os

if __name__ == '__main__':
    print("run app use `python -m app.*`\n\ninstall app list:\n"+"\n".join([f for f in next(dirs for _,dirs,_ in os.walk(os.path.split(sys.argv[0])[0])) if not f.startswith("_")]))