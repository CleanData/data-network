# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Organization.name'
        db.alter_column(u'data_connections_organization', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'ContributorRelation.work_done'
        db.alter_column(u'data_connections_contributorrelation', 'work_done', self.gf('django.db.models.fields.TextField')(max_length=10))

    def backwards(self, orm):

        # Changing field 'Organization.name'
        db.alter_column(u'data_connections_organization', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'ContributorRelation.work_done'
        db.alter_column(u'data_connections_contributorrelation', 'work_done', self.gf('django.db.models.fields.TextField')(max_length=20000))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data_connections.contributorrelation': {
            'Meta': {'object_name': 'ContributorRelation'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_data'", 'to': u"orm['data_connections.UserProfile']"}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_contributor'", 'to': u"orm['data_connections.Dataset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_done': ('django.db.models.fields.TextField', [], {'max_length': '10'})
        },
        u'data_connections.datacatalog': {
            'Meta': {'object_name': 'DataCatalog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'managed_datacatalogs'", 'to': u"orm['data_connections.UserProfile']"}),
            'managing_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'managed_datacatalogs'", 'null': 'True', 'to': u"orm['data_connections.Organization']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'data_connections.datarelation': {
            'Meta': {'object_name': 'DataRelation'},
            'derivative': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_source'", 'to': u"orm['data_connections.Dataset']"}),
            'how_data_was_processed': ('django.db.models.fields.TextField', [], {'max_length': '20000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_derivative'", 'to': u"orm['data_connections.Dataset']"})
        },
        u'data_connections.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contributed_datasets'", 'to': u"orm['data_connections.UserProfile']", 'through': u"orm['data_connections.ContributorRelation']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'data_catalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_connections.DataCatalog']", 'null': 'True', 'blank': 'True'}),
            'data_format': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'formatted_datasets'", 'null': 'True', 'to': u"orm['data_connections.Format']"}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'licensed_datasets'", 'null': 'True', 'to': u"orm['data_connections.License']"}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'managed_datasets'", 'null': 'True', 'to': u"orm['data_connections.UserProfile']"}),
            'managing_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'managed_datasets'", 'null': 'True', 'to': u"orm['data_connections.Organization']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'derivatives'", 'to': u"orm['data_connections.Dataset']", 'through': u"orm['data_connections.DataRelation']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'data_connections.format': {
            'Meta': {'object_name': 'Format'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'data_connections.license': {
            'Meta': {'object_name': 'License'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'data_connections.membershiprelation': {
            'Meta': {'object_name': 'MembershipRelation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_organization'", 'to': u"orm['data_connections.UserProfile']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_member'", 'to': u"orm['data_connections.Organization']"})
        },
        u'data_connections.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data_connections.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'collaborators_rel_+'", 'to': u"orm['data_connections.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['data_connections']