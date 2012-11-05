# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'State'
        db.create_table('app_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('app', ['State'])

        # Adding model 'City'
        db.create_table('app_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.State'])),
        ))
        db.send_create_signal('app', ['City'])

        # Adding model 'UserProfile'
        db.create_table('app_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('verification_key', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('key_expires', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('home_town', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('facebook_username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('facebook_email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('twitter_username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('twitter_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('google_username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('google_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('google_email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('time_zone', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('app', ['UserProfile'])

        # Adding model 'PriceModel'
        db.create_table('app_pricemodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price_per_hour', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=16, decimal_places=2)),
            ('price_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('app', ['PriceModel'])

        # Adding model 'Album'
        db.create_table('app_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('cover_photo', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('app', ['Album'])

        # Adding model 'AlbumImage'
        db.create_table('app_albumimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Album'])),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('thumbnail', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('preview', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('app', ['AlbumImage'])


    def backwards(self, orm):
        # Deleting model 'State'
        db.delete_table('app_state')

        # Deleting model 'City'
        db.delete_table('app_city')

        # Deleting model 'UserProfile'
        db.delete_table('app_userprofile')

        # Deleting model 'PriceModel'
        db.delete_table('app_pricemodel')

        # Deleting model 'Album'
        db.delete_table('app_album')

        # Deleting model 'AlbumImage'
        db.delete_table('app_albumimage')


    models = {
        'app.album': {
            'Meta': {'object_name': 'Album'},
            'cover_photo': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
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