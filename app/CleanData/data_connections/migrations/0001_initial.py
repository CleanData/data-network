# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataCatalog'
        db.create_table(u'data_connections_datacatalog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='managed_datacatalogs', null=True, to=orm['data_connections.UserProfile'])),
            ('managing_organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='managed_datacatalogs', null=True, to=orm['data_connections.Organization'])),
        ))
        db.send_create_signal(u'data_connections', ['DataCatalog'])

        # Adding model 'License'
        db.create_table(u'data_connections_license', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'data_connections', ['License'])

        # Adding model 'Format'
        db.create_table(u'data_connections_format', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'data_connections', ['Format'])

        # Adding model 'Dataset'
        db.create_table(u'data_connections_dataset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_catalog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data_connections.DataCatalog'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('data_format', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='formatted_datasets', null=True, to=orm['data_connections.Format'])),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='licensed_datasets', null=True, to=orm['data_connections.License'])),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='managed_datasets', null=True, to=orm['data_connections.Scientist'])),
            ('managing_organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='managed_datasets', null=True, to=orm['data_connections.Organization'])),
        ))
        db.send_create_signal(u'data_connections', ['Dataset'])

        # Adding unique constraint on 'Dataset', fields ['name', 'url']
        db.create_unique(u'data_connections_dataset', ['name', 'url'])

        # Adding model 'DataRelation'
        db.create_table(u'data_connections_datarelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_to_derivative', to=orm['data_connections.Dataset'])),
            ('derivative', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_to_source', to=orm['data_connections.Dataset'])),
            ('how_data_was_processed', self.gf('django.db.models.fields.TextField')(max_length=20000, blank=True)),
        ))
        db.send_create_signal(u'data_connections', ['DataRelation'])

        # Adding model 'Scientist'
        db.create_table(u'data_connections_scientist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('profile_url', self.gf('django.db.models.fields.URLField')(default='', max_length=150, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['data_connections.UserProfile'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'data_connections', ['Scientist'])

        # Adding unique constraint on 'Scientist', fields ['firstname', 'lastname', 'profile_url']
        db.create_unique(u'data_connections_scientist', ['firstname', 'lastname', 'profile_url'])

        # Adding M2M table for field collaborators on 'Scientist'
        m2m_table_name = db.shorten_name(u'data_connections_scientist_collaborators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_scientist', models.ForeignKey(orm[u'data_connections.scientist'], null=False)),
            ('to_scientist', models.ForeignKey(orm[u'data_connections.scientist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_scientist_id', 'to_scientist_id'])

        # Adding model 'UserProfile'
        db.create_table(u'data_connections_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'data_connections', ['UserProfile'])

        # Adding model 'Organization'
        db.create_table(u'data_connections_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=150)),
        ))
        db.send_create_signal(u'data_connections', ['Organization'])

        # Adding model 'MembershipRelation'
        db.create_table(u'data_connections_membershiprelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_to_member', to=orm['data_connections.Organization'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_to_organization', to=orm['data_connections.Scientist'])),
        ))
        db.send_create_signal(u'data_connections', ['MembershipRelation'])

        # Adding model 'ContributorRelation'
        db.create_table(u'data_connections_contributorrelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_to_data', to=orm['data_connections.Scientist'])),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_to_contributor', to=orm['data_connections.Dataset'])),
            ('work_done', self.gf('django.db.models.fields.TextField')(max_length=20000, blank=True)),
        ))
        db.send_create_signal(u'data_connections', ['ContributorRelation'])


    def backwards(self, orm):
        # Removing unique constraint on 'Scientist', fields ['firstname', 'lastname', 'profile_url']
        db.delete_unique(u'data_connections_scientist', ['firstname', 'lastname', 'profile_url'])

        # Removing unique constraint on 'Dataset', fields ['name', 'url']
        db.delete_unique(u'data_connections_dataset', ['name', 'url'])

        # Deleting model 'DataCatalog'
        db.delete_table(u'data_connections_datacatalog')

        # Deleting model 'License'
        db.delete_table(u'data_connections_license')

        # Deleting model 'Format'
        db.delete_table(u'data_connections_format')

        # Deleting model 'Dataset'
        db.delete_table(u'data_connections_dataset')

        # Deleting model 'DataRelation'
        db.delete_table(u'data_connections_datarelation')

        # Deleting model 'Scientist'
        db.delete_table(u'data_connections_scientist')

        # Removing M2M table for field collaborators on 'Scientist'
        db.delete_table(db.shorten_name(u'data_connections_scientist_collaborators'))

        # Deleting model 'UserProfile'
        db.delete_table(u'data_connections_userprofile')

        # Deleting model 'Organization'
        db.delete_table(u'data_connections_organization')

        # Deleting model 'MembershipRelation'
        db.delete_table(u'data_connections_membershiprelation')

        # Deleting model 'ContributorRelation'
        db.delete_table(u'data_connections_contributorrelation')


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
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['data_connections']