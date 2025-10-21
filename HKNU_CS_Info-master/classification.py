import json

class Classification:
    def makeG4(self, a, b, c, d, e, deleted):
        result = []

        for data in a:
            if '졸업' in data['제목'] and data['제목'] not in deleted:
                result.append(data)

        for data in b:
            if '졸업' in data['제목'] and data['제목'] not in deleted:
                result.append(data)

        for data in c:
            if '졸업' in data['제목'] and data['제목'] not in deleted:
                result.append(data)

        for data in d:
            if data['제목'] not in deleted:
                result.append(data)

        for data in e:
            if data['제목'] not in deleted:
                result.append(data)

        result = sorted(result, key=lambda x: x['작성일'])[-10:]

        return result

    def makeG23(self, a, b, c, deleted):
        result = []

        for data in a:
            if '졸업' not in data['제목'] and data['제목'] not in deleted:
                result.append(data)

        for data in b:
            if '졸업' not in data['제목'] and data['제목'] not in deleted:
                result.append(data)

        for data in c:
            if '졸업' not in data['제목'] and data['제목'] not in deleted:
                result.append(data)

        result = sorted(result, key=lambda x: x['작성일'])[-10:]

        return result

    def process_data(self):

        # JSON 파일 읽기
        with open('json/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 'haksa'의 내용 출력
        haksa = data.get('haksa', [])
        janghak = data.get('janghak', [])
        hankyong = data.get('hankyong', [])
        chaeyong = data.get('chaeyong', [])
        changup = data.get('changup', [])
        deleted = data.get('deleted', [])

        g4 = self.makeG4(haksa, janghak, hankyong, chaeyong, changup, deleted)
        g23 = self.makeG23(haksa, janghak, hankyong, deleted)

        classified_data = {'g23': g23, 'g4': g4}

        with open('json/classified_data.json', 'w', encoding='utf-8') as file:
            json.dump(classified_data, file, ensure_ascii=False, indent=4)