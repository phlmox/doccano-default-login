import os,sys,requests,argparse
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings()

parser=argparse.ArgumentParser(
        prog='doccano_default',
        description='Doccano Default Credentials Check',
        epilog='by @phlmox | Github: https://github.com/phlmox/')

parser.add_argument('-u','--url',help='Single URL')
parser.add_argument('-U','--urls',help='Filename that contains urls')
parser.add_argument('-d','--dont-check',help='Don\'t check if the target is really doccano or not')
parser.add_argument('-o','--output',help='Save hosts to output file')

args=parser.parse_args()

if not args.url and not args.urls:
        print("You need to specify at least one url!\n")
        parser.print_help(sys.stderr)
        sys.exit(0)

urls=[args.url] if args.url!=None else open(args.urls,"r").read().split(os.linesep)[:-1]
routes=["/v1/auth/login/","/v1/auth-token"]
found=[]
for url in urls:
        u=urlparse(url)
        u=u.scheme+"://"+u.netloc
        print("[+] Testing "+u)
        s=requests.Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; PPC Mac OS X 10.5; rv:31.0) Gecko/20100101 Firefox/31.0 TenFourFox/7450'})
        try:
                r = s.get(u,verify=False)
                if "doccano is an open source annotation tools" not in r.text:
                        print(f"[-] Target {u} is not doccano! If you sure target is using doccano, run the program with --dont-check flag")
        except KeyboardInterrupt:
                print("Exiting...")
                sys.exit(0)
        except:
                print("[-] Can't reach target "+u)
                continue

        for r in routes:
                try:
                        ar = requests.post(u+r,verify=False,headers={"Content-Type":"application/json;charset=UTF-8"},data='{"username":"admin","password":"password"}')
                        if any(x in ar.text for x in ['"token":','"key":']):
                                print("[+] Yaay: "+u)
                                found.append(u)
                        if "Unable to log in with provided credentials" in ar.text:
                                passed=False
                                print("[-] Nope: "+u)
                                break
                except:pass

if args.output:
        with open(args.output,"w") as f:
                for u in found:f.write(u+os.linesep)

print(f"Found total {len(found)} doccano hosts using default credentials (admin/password).")
print("by @phlmox | https://twitter.com/EnesSaltk7")
