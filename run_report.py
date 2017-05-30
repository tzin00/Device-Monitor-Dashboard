import requests


def main():
    req = requests.post('http://localhost:8000/check-hosts', data={})
    print(req.status_code, req.reason)

if __name__ == '__main__':
    main()