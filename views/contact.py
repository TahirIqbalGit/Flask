from flask import Blueprint, render_template, request

contact = Blueprint('contact', __name__)
# connect to your Mongo DB database
# client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@clusterforproject.ddxhn.mongodb.net/{database}?"
#                              + "retryWrites=true&w=majority")
# # get the database name
# db = client.get_database(database)
# # get the particular collection that contains the data
# records = db.contact


@contact.route("/contact", methods=['GET', 'POST'])
def contact_page():
    req = request.form
    print(req)
    if request.method == "POST":
        # Validating Empty Fields
        missing = list()
        # Getting Immutable Multi Dict Data
        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            comment = f"Missing field: {',  '.join(missing)}".title()
            return comment
            # return render_template("contact.html", success=False, comment=comment, miss=True, is_email=False)
        else:
            # getting form data
            name = req.get("name")
            # request.form["name"]
            email = req.get("email")
            subject = req.get("subject")
            phone = req.get("phone")
            message = req.get("message")
            # if email found in database showcase that it's found
            # email_found = records.find_one({"email": email})
            # if email_found:
            #     comment = "This email is already listed, try another one"
            #     return comment
            input_data = {
                "name": name,
                "email": email,
                "subject": subject,
                "phone": phone,
                "message": message
            }
            # insert input data in record collection
            # records.insert_one(input_data)
            comment = "Thanks for contacting us! We'll respond you as soon as possible"
            return comment
            # return render_template("contact.html", success=True, comment=comment, miss=False, is_email=False)
    else:
        return render_template("contact.html")
