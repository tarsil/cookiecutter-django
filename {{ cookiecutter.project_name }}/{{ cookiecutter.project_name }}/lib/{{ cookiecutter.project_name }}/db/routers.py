from django.conf import settings


class MongoDBRouter:

    db_name = 'mongodb'
    default_db = "default"
    route_app_labels = {"blockchain", "socialmedia"}
    
    def db_for_read(self, model, **hints):
        """
        Attempts to read Mongo models go to mongo database.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.db_name
        return self.default_db
    
    def db_for_write(self, model, **hints):
        """
        Attempts to write mongo models go to the mongo database.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.db_name
        return self.default_db
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Do not allow relations involving the remote database
        """
        if obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels:
           return False
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Do not allow migrations on the remote database
        """
        if app_label in self.route_app_labels:
            return False
        return True
