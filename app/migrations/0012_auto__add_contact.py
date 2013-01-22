# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table('app_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('inquiry', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table('app_contact')


    models = {
        'app.album': {
            'Meta': {'object_name': 'Album'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category'", 'null': 'True', 'to': "orm['app.AlbumCategory']"}),
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.College']", 'null': 'True', 'blank': 'True'}),
            'cover_photo': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'points': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '16', 'decimal_places': '9'}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subcategory'", 'null': 'True', 'to': "orm['app.AlbumCategory']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'app.albumcategory': {
            'Meta': {'object_name': 'AlbumCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.AlbumCategory']", 'null': 'True', 'blank': 'True'})
        },
        'app.albumimage': {
            'Meta': {'object_name': 'AlbumImage'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Album']"}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'preview': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'top': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'app.albumimagevote': {
            'Meta': {'object_name': 'AlbumImageVote'},
            'album_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.AlbumImage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'app.albumvote': {
            'Meta': {'object_name': 'AlbumVote'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Album']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'app.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.State']"})
        },
        'app.college': {
            'Meta': {'object_name': 'College'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'app.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inquiry': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'app.eventbooking': {
            'Meta': {'object_name': 'EventBooking'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendarapp.EventObject']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_key': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
        'calendarapp.eventobject': {
            'Meta': {'object_name': 'EventObject'},
            'all_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'background_color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'db_column': "'background_color'", 'blank': 'True'}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'class_name'", 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'db_column': "'color'", 'blank': 'True'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'event_type'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'independent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'text_color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'db_column': "'text_color'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'db_column': "'url'", 'blank': 'True'})
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