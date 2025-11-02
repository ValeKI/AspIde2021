import random

if __name__ == '__main__':
    letters = 'qwertyuiopasdfghjklzxcvbnmQAWSEDRFTGYHUJIKOLPZXCVBNM1234567890'
    for x in range(0, 14):
        for i in range(0, 100):
            print(letters[random.randint(0, len(letters) - 1)], end='')
        print('\n----------')
