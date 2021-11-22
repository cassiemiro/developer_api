from models import Person


def insert():
    person = Person(name="Cassiemiro", age=22)
    person.save()


def query():
    persons = Person.query.all()

    for person in persons:
        print("name:", person.name + " age", person.age)

    # person = Person.query.filter_by(name="Felipe").first()
    # print("Filter by name", person)


def alter():
    person = Person.query.filter_by(name="felipe").first()
    person.age = 21
    person.name = "Gilena"
    person.save()


def delete():
    person = Person.query.filter_by(name="NonExist").first()
    person.delete()


if __name__ == "__main__":
    # insert()
    alter()
    # delete()
    query()
