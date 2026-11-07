"""Task 14: JSON-backed command-line contact manager."""

import json
import os

DATA_FILE = "contacts.json"


def load_contacts(path=DATA_FILE):
    if not os.path.exists(path):
        return {}

    try:
        with open(path, encoding="utf-8") as file:
            contacts = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Contact file is corrupt; original file preserved: {exc}")

    if not isinstance(contacts, dict):
        raise ValueError("Contact data must be a JSON object")

    return contacts


def save_contacts(contacts, path=DATA_FILE):
    temp_path = path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)
    os.replace(temp_path, path)


def add_contact(contacts, contact_id, name, phone, email):
    if contact_id in contacts:
        raise ValueError("Contact ID already exists")
    if not name.strip():
        raise ValueError("Name cannot be empty")

    contacts[contact_id] = {
        "id": contact_id,
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
    }


def search_contacts(contacts, query):
    query = query.casefold()
    matches = []
    for contact in contacts.values():
        if query in contact["name"].casefold():
            matches.append(contact)
    return matches


def update_contact(contacts, contact_id, **changes):
    if contact_id not in contacts:
        raise KeyError("Contact not found")

    for field in ("name", "phone", "email"):
        if field in changes:
            value = str(changes[field]).strip()
            if field == "name" and not value:
                raise ValueError("Name cannot be empty")
            contacts[contact_id][field] = value


def delete_contact(contacts, contact_id):
    if contact_id not in contacts:
        raise KeyError("Contact not found")
    del contacts[contact_id]


def main():
    contacts = load_contacts()

    while True:
        print("\n1 Add  2 Search  3 Update  4 Delete  5 List  0 Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                contact_id = input("ID: ").strip()
                name = input("Name: ")
                phone = input("Phone: ")
                email = input("Email: ")
                add_contact(contacts, contact_id, name, phone, email)
                save_contacts(contacts)

            elif choice == "2":
                query = input("Name search: ")
                for contact in search_contacts(contacts, query):
                    print(contact)

            elif choice == "3":
                contact_id = input("ID: ").strip()
                name = input("New name: ")
                phone = input("New phone: ")
                email = input("New email: ")
                update_contact(
                    contacts,
                    contact_id,
                    name=name,
                    phone=phone,
                    email=email,
                )
                save_contacts(contacts)

            elif choice == "4":
                contact_id = input("ID: ").strip()
                delete_contact(contacts, contact_id)
                save_contacts(contacts)

            elif choice == "5":
                for contact in contacts.values():
                    print(contact)

            elif choice == "0":
                break

            else:
                print("Invalid choice")

        except (ValueError, KeyError) as exc:
            print("Error:", exc)


if __name__ == "__main__":
    main()
