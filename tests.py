from pickle import TRUE
from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, USER, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the 
        # User model below.
        Post.query.delete()
        USER.query.delete()

        self.client = app.test_client()

        self.test_user = USER(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)
        # self.test_post = Post(title="Soccer",
        #                             content="It's fun!",
        #                             created_at="2022-02-03 6:00",
        #                             user_id=1)

        # second_user = USER(first_name="test_first_two", last_name="test_last_two",
        #                    image_url=None)

        self.sample_data = {
            'first_name' : 'Phil', 
            'last_name' : 'Jackson', 
            'image_url': 'None'}
        
        self.sample_post = {
            'post_title': 'Basket',
            'post_content': 'Great to watch games!'
        }
    

        db.session.add_all([self.test_user])
        db.session.commit()
        self.user_id = self.test_user.id
        self.test_post = Post(title="Soccer",
                                    content="It's fun!",
                                    created_at="2022-02-03 6:00",
                                    user_id=self.user_id)

        db.session.add_all([self.test_post])
        db.session.commit()


        # We can hold onto our test_user's id by attaching it to self (which is 
        # accessible throughout this test class). This way, we'll be able to 
        # rely on this user in our tests without needing to know the numeric 
        # value of their id, since it will change each time our tests are run. 
        
        self.post_id = self.test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests to show main page correctly"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_add_new_user(self):
        """Tests that Add New User is succesfully added"""
        with self.client as c:
            resp = c.post('/users/new', data=self.sample_data)
            self.assertEqual(resp.status_code, 302)

            resp = c.get('/users', follow_redirects = True)

            html = resp.get_data(as_text=True)
            self.assertIn('Phil', html)
            self.assertIn('Jackson', html)

    def test_update_user_info(self):
        """Tests that user info is successfully updated"""
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/edit', data=self.sample_data)
            self.assertEqual(resp.status_code, 302)

            resp = c.get('/users', follow_redirects = True)
            html = resp.get_data(as_text=True)
            self.assertNotEqual("test_first", "Phil")
            self.assertNotIn("test_first", html)

    def test_delete_user_info(self):
        """Tests that user info is successfully deleted"""
        with self.client as c:
            Post.query.filter(Post.id == self.post_id).delete()
            resp = c.post(f'/users/{self.user_id}/delete')

            self.assertEqual(resp.status_code, 302)
            
            resp = c.get('/users', follow_redirects = True)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test_first", html)
            self.assertNotIn("test_last", html)

    #  tests for posts

    def test_show_users_detail(self):
        """Tests to show user detail page"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_add_new_post(self):
        """Tests that new post is succesfully added"""
        with self.client as c:
            resp = c.post((f'/users/{self.user_id}/posts/new'), data=self.sample_post)
            self.assertEqual(resp.status_code, 302)

            resp = c.get(f'/users/{self.user_id}', follow_redirects = True)

            html = resp.get_data(as_text=True)
            self.assertIn('Soccer', html)
            # self.assertIn("It's fun!", html)

    def test_update_post_info(self):
        """Tests that user info is successfully updated"""
        with self.client as c:
            resp = c.post(f'/posts/{self.post_id}/edit', data=self.sample_post)
            self.assertEqual(resp.status_code, 302)

            resp = c.get(f'/posts/{self.post_id}', follow_redirects = True)
            html = resp.get_data(as_text=True)
            self.assertNotIn("Soccer", html)
            self.assertIn("Basket", html)

    def test_delete_post_info(self):
        """Tests that user info is successfully deleted"""
        with self.client as c:
            resp = c.post(f'/posts/{self.post_id}/delete')
            self.assertEqual(resp.status_code, 302)
            
            resp = c.get(f'/users/{self.user_id}', follow_redirects = True)
            html = resp.get_data(as_text=True)
            self.assertNotIn("Soccer", html)
            self.assertNotIn("It's fun!", html)