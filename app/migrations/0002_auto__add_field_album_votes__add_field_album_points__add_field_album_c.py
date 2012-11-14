# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Album.votes'
        db.add_column('app_album', 'votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Album.points'
        db.add_column('app_album', 'points',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=16, decimal_places=9),
                      keep_default=False)

        # Adding field 'Album.created_date'
        db.add_column('app_album', 'created_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 11, 14, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Album.votes'
        db.delete_column('app_album', 'votes')

        # Deleting field 'Album.points'
        db.delete_column('app_album', 'points')

        # Deleting field 'Album.created_date'
        db.delete_column('app_album', 'created_date')


    models = {
        'app.album': {
            'Meta': {'object_name': 'Album'},
            'cover_photo': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'points': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '16', 'decimal_places': '9'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'app.albumimage': {
            'Meta': {'object_name': 'AlbumImage'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Album']"}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'preview': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'app.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.State']"})
        },
        'app.pricemodel': {
            'Meta': {'object_name': 'PriceModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_per_hour': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '16', 'decimal_places': '2'}),
            'price_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'app.state': {
            'Meta': {'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'facebook_email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'facebook_username': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'google_email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'google_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'google_username': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'home_town': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'verification_key': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']