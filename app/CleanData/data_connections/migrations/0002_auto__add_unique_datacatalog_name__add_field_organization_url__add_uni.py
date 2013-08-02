# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Dataset', fields ['url']
        db.delete_unique(u'data_connections_dataset', ['url'])

        # Adding model 'Scientist'
        db.create_table(u'data_connections_scientist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('profile_url', self.gf('django.db.models.fields.URLField')(default='', max_length=150, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['data_connections.UserProfile'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'data_connections', ['Scientist'])

        # Adding M2M table for field collaborators on 'Scientist'
        m2m_table_name = db.shorten_name(u'data_connections_scientist_collaborators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_scientist', models.ForeignKey(orm[u'data_connections.scientist'], null=False)),
            ('to_scientist', models.ForeignKey(orm[u'data_connections.scientist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_scientist_id', 'to_scientist_id'])

        # Adding unique constraint on 'Scientist', fields ['firstname', 'lastname', 'profile_url']
        db.create_unique(u'data_connections_scientist', ['firstname', 'lastname', 'profile_url'])


        # Changing field 'DataCatalog.manager'
        db.alter_column(u'data_connections_datacatalog', 'manager_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['data_connections.UserProfile']))
        # Adding unique constraint on 'DataCatalog', fields ['name']
        db.create_unique(u'data_connections_datacatalog', ['name'])

        # Adding field 'Organization.url'
        db.add_column(u'data_connections_organization', 'url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=150),
                      keep_default=False)

        # Adding unique constraint on 'Organization', fields ['name']
        db.create_unique(u'data_connections_organization', ['name'])


        # Changing field 'ContributorRelation.contributor'
        db.alter_column(u'data_connections_contributorrelation', 'contributor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data_connections.Scientist']))

        # Changing field 'Dataset.manager'
        db.alter_column(u'data_connections_dataset', 'manager_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['data_connections.Scientist']))
        # Removing M2M table for field collaborators on 'UserProfile'
        db.delete_table(db.shorten_name(u'data_connections_userprofile_collaborators'))

        # Adding unique constraint on 'Format', fields ['name']
        db.create_unique(u'data_connections_format', ['name'])


        # Changing field 'MembershipRelation.member'
        db.alter_column(u'data_connections_membershiprelation', 'member_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data_connections.Scientist']))
        # Adding unique constraint on 'License', fields ['name']
        db.create_unique(u'data_connections_license', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'License', fields ['name']
        db.delete_unique(u'data_connections_license', ['name'])

        # Removing unique constraint on 'Format', fields ['name']
        db.delete_unique(u'data_connections_format', ['name'])

        # Removing unique constraint on 'Organization', fields ['name']
        db.delete_unique(u'data_connections_organization', ['name'])

        # Removing unique constraint on 'DataCatalog', fields ['name']
        db.delete_unique(u'data_connections_datacatalog', ['name'])

        # Removing unique constraint on 'Scientist', fields ['firstname', 'lastname', 'profile_url']
        db.delete_unique(u'data_connections_scientist', ['firstname', 'lastname', 'profile_url'])

        # Deleting model 'Scientist'
        db.delete_table(u'data_connections_scientist')

        # Removing M2M table for field collaborators on 'Scientist'
        db.delete_table(db.shorten_name(u'data_connections_scientist_collaborators'))


        # Changing field 'DataCatalog.manager'
        db.alter_column(u'data_connections_datacatalog', 'manager_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['data_connections.UserProfile']))
        # Deleting field 'Organization.url'
        db.delete_column(u'data_connections_organization', 'url')


        # Changing field 'ContributorRelation.contributor'
        db.alter_column(u'data_connections_contributorrelation', 'contributor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data_connections.UserProfile']))
        # Adding unique constraint on 'Dataset', fields ['url']
        db.create_unique(u'data_connections_dataset', ['url'])


        # Changing field 'Dataset.manager'
        db.alter_column(u'data_connections_dataset', 'manager_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['data_connections.UserProfile']))
        # Adding M2M table for field collaborators on 'UserProfile'
        m2m_table_name = db.shorten_name(u'data_connections_userprofile_collaborators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm[u'data_connections.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm[u'data_connections.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_userprofile_id', 'to_userprofile_id'])


        # Changing field 'MembershipRelation.member'
        db.alter_column(u'data_connections_membershiprelation', 'member_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data_connections.UserProfile']))

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
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_data'", 'to': u"orm['data_connections.Scientist']"}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_contributor'", 'to': u"orm['data_connections.Dataset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_done': ('django.db.models.fields.TextField', [], {'max_length': '20000', 'blank': 'True'})
        },
        u'data_connections.datacatalog': {
            'Meta': {'object_name': 'DataCatalog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'managed_datacatalogs'", 'null': 'True', 'to': u"orm['data_connections.UserProfile']"}),
            'managing_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'managed_datacatalogs'", 'null': 'True', 'to': u"orm['data_connections.Organization']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'data_connections.datarelation': {
            'Meta': {'object_name': 'DataRelation'},
            'derivative': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_source'", 'to': u"orm['data_connections.Dataset']"}),
            'how_data_was_processed': ('django.db.models.fields.TextField', [], {'max_length': '20000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_derivative'", 'to': u"orm['data_connections.Dataset']"})
        },
        u'data_connections.dataset': {
            'Meta': {'unique_together': "(('name', 'url'),)", 'object_name': 'Dataset'},
            'contributors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contributed_datasets'", 'to': u"orm['data_connections.Scientist']", 'through': u"orm['data_connections.ContributorRelation']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'data_catalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_connections.DataCatalog']", 'null': 'True', 'blank': 'True'}),
            'data_format': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'formatted_datasets'", 'null': 'True', 'to': u"orm['data_connections.Format']"}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'licensed_datasets'", 'null': 'True', 'to': u"orm['data_connections.License']"}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'managed_datasets'", 'null': 'True', 'to': u"orm['data_connections.Scientist']"}),
            'managing_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'managed_datasets'", 'null': 'True', 'to': u"orm['data_connections.Organization']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'derivatives'", 'to': u"orm['data_connections.Dataset']", 'through': u"orm['data_connections.DataRelation']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150'})
        },
        u'data_connections.format': {
            'Meta': {'object_name': 'Format'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'data_connections.license': {
            'Meta': {'object_name': 'License'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'data_connections.membershiprelation': {
            'Meta': {'object_name': 'MembershipRelation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_organization'", 'to': u"orm['data_connections.Scientist']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to_member'", 'to': u"orm['data_connections.Organization']"})
        },
        u'data_connections.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '150'})
        },
        u'data_connections.scientist': {
            'Meta': {'unique_together': "(('firstname', 'lastname', 'profile_url'),)", 'object_name': 'Scientist'},
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'collaborators_rel_+'", 'to': u"orm['data_connections.Scientist']"}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['data_connections.UserProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'data_connections.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['data_connections']