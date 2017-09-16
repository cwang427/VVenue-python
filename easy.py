import cognitive_face as CF
KEY = '26a1c49867934418bfcceac915443574'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

print CF.person.lists("id1")