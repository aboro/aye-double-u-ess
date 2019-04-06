import requests
import argparse
import os
import configparser

def setup_conf(config):
  file = open("config.ini", "w")
  print("Set up your access key and buckets")
  config.add_section("Config")
  access_key = input("Enter access key value:")
  secret_key = input("Enter secret key value:")
  bucket = input("Enter bucket name:")
  config.set("Config","access-key",access_key)
  config.set("Config","secret-key",secret_key)
  config.set("Config","bucketName",bucket)
  config.write(file)
  file.close()
  return config

def ls(args, config):
  headers = {}
  headers['access-key'] = config['access-key']
  headers['secret-key'] = config['secret-key']
  if isinstance(args.S4Uri,type(None)):
    headers['method'] = "ls"
    headers['bucke-name'] = config['bucketName']
  elif "s4://" in args.S4Uri:
    temp = args.S4Uri[5:]
    headers['item'] = temp[temp.find("/")+1:]
    headers['method'] = "ls"
    headers['bucket-name'] = temp[:temp.find("/")]
    print(args.S4Uri[5:])  
  elif "/" in args.S4Uri:
    temp = args.S4Uri
    headers['item'] = temp[temp.find("/")+1:]
    print(temp)  
  else:
    headers['item'] = args.S4Uri
    headers['method'] = "ls"
    headers['bucket-name'] = config['bucketName']

  print(headers)
  response = requests.get("http://web3.crikey.ctf:8080", headers=headers)
  return response.text

def cp(args, config):
  headers = {}
  headers['access-key'] = config['access-key']
  headers['secret-key'] = config['secret-key']
  response = requests.get("http://web3.crikey.ctf:8080", headers=headers)
  return response.text
  
def setup_parser():
  parser = argparse.ArgumentParser(description='Change the option prefix characters',prefix_chars='-',)
  parser.add_argument("s4", help="The service to use (hint: there's only s4)", type=str)
  # Now handle if ls or cp
  subparsers = parser.add_subparsers(help='sub-command help')
  parser_ls = subparsers.add_parser('ls', help='ls help')
  parser_ls.add_argument("S4Uri", nargs='?', help="s4://bucketname or None", type=str)
  parser_ls.set_defaults(func=ls)

  parser_cp = subparsers.add_parser('cp', help='cp help')
  parser_cp.add_argument("<filename>", nargs=2, help="S4Uri and localfile or localfile and S4Uri", type=str)
  parser_cp.set_defaults(func=cp)
   
  return parser
  
def main():
  # flag{aye_double_u_ess_s4_tool}
  # Set up or read config if it exists
  config = configparser.ConfigParser()
  
  if not os.path.exists("config.ini"):
    config = setup_conf(config)
  else:
    try:
      config.read("config.ini")
      key_test = config["Config"]["access-key"]
    except:
      print("An error occurred with your config file, please recreate it")
      config = setup_conf(config)
  
  # Simplify access
  config = config['Config']
  parser = setup_parser()
  args = parser.parse_args()
  try:
    print(args.func(args, config))
  except AttributeError:
    parser.print_help()
  
if __name__ == "__main__":
  main()
