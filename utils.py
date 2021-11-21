from models import People


def insert():
    person = People(name="NonExist", age=19)
    person.save()


def query():
    people = People.query.all()

    for person in people:
        print("name:", person.name + " age", person.age)

    # person = People.query.filter_by(name="Felipe").first()
    # print("Filter by name", person)


def alter():
    person = People.query.filter_by(name="NonExist").first()
    person.age = 21
    person.save()


def delete():
    person = People.query.filter_by(name="NonExist").first()
    person.delete()


if __name__ == "__main__":
    # insert()
    # alter()
    delete()
    query()
