select type, field_statement_id_value as 'statement_id', title, field_statement_title_value as "statement title", field_statement_date_value as 'statement_date', field_issue_date_value as 'issue_date', field_author_value as 'author',  field_produced_by_value as 'produced_by', field_released_by_value as 'released_by', uid as 'posted_by', field_media_type_value as 'media_type', field_access_value as 'access', field_full_text_url as 'full_text_url', th.`parent` as 'context', td.`name` as 'keyword'

from gtrp.node n
join gtrp.field_data_field_statement_title t on t.entity_id = n.nid
join gtrp.field_data_field_statement_id e on e.entity_id = n.nid 
join gtrp.field_data_field_statement_date d on d.entity_id = n.nid
join gtrp.field_data_field_issue_date issued on issued.entity_id = n.nid
join gtrp.field_data_field_author auth on auth.entity_id = n.nid
join gtrp.field_data_field_produced_by prod on prod.entity_id = n.nid
join gtrp.field_data_field_released_by relea on relea.entity_id = n.nid
join gtrp.field_data_field_media_type med on med.entity_id = n.nid
join gtrp.field_data_field_full_text urls on urls.entity_id = n.nid
join gtrp.field_data_field_access doa on doa.entity_id = n.nid  
join gtrp.taxonomy_index ti on n.nid = ti.nid
join gtrp.taxonomy_term_data td on ti.tid = td.tid
join gtrp.taxonomy_term_hierarchy th on ti.tid = th.tid  
where status = 1;


node id, run it through taxonomy index, gives you a tid, for a partiucular thing it can give 22 tids. If you run that through term_data then you get a name, but some entries have a parent. the taxonomy hiearchy gives the


--title
field_data_field_statement_title    field_statement_title_value

--statement id (ex. AAM20101023)
field_data_field_statement_id   field_statement_id_value

--issue date
field_data_field_issue_date		field_issue_date_value

-- statement date
field_data_field_statement_date   field_statement_date_value

--author
field_data_field_author   field_author_value

--produced by
field_data_field_produced_by		field_produced_by_value

--released by
field_data_field_released_by		field_released_by_value

--media type
field_data_field_media_type		field_media_type_value

--access 
field_data_field_access   field_access_value

--full-text
field_data_field_full_text		field_full_text_title

--organization
field_data_field_jihad_organization		field_jihad_organization_value

-- posted by
node uid (users uid)

--keywords ??
taxonomy_term_data  name tid vid

-- contexts?? (ex. 0000503-Counterislamic Propaganda)
taxonomy_term_lineage   lineage  




