# Generated by Django 4.0 on 2024-04-18 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sign', '0001_initial'),
        ('flow', '0001_initial'),
        ('richmenu', '0001_initial'),
        ('template', '0001_initial'),
        ('question', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userflowschedule',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_history', to='question.shopquestion'),
        ),
        migrations.AddField(
            model_name='userflowactionreminder',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_reminder', to='flow.userflow'),
        ),
        migrations.AddField(
            model_name='userflowactionreminder',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_reminder', to='template.shoptemplatecardtype'),
        ),
        migrations.AddField(
            model_name='userflowactionreminder',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_reminder', to='template.shoptemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='userflowactionreminder',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_reminder', to='template.shoptemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='userflowactionreminder',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_reminder', to='template.shoptemplatetext'),
        ),
        migrations.AddField(
            model_name='userflowactionreminder',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_reminder', to='template.shoptemplatevideo'),
        ),
        migrations.AddField(
            model_name='userflowactionreminder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_reminder', to='user.lineuser'),
        ),
        migrations.AddField(
            model_name='userflowactionmessage',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_message', to='flow.userflow'),
        ),
        migrations.AddField(
            model_name='userflowactionmessage',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_message', to='template.shoptemplatecardtype'),
        ),
        migrations.AddField(
            model_name='userflowactionmessage',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_message', to='template.shoptemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='userflowactionmessage',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_message', to='template.shoptemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='userflowactionmessage',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_message', to='template.shoptemplatetext'),
        ),
        migrations.AddField(
            model_name='userflowactionmessage',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_message', to='template.shoptemplatevideo'),
        ),
        migrations.AddField(
            model_name='userflowactionmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_action_message', to='user.lineuser'),
        ),
        migrations.AddField(
            model_name='userflow',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_flow', to='flow.shopflow'),
        ),
        migrations.AddField(
            model_name='userflow',
            name='flow_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='userflow',
            name='flow_tab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow', to='flow.shopflowtab'),
        ),
        migrations.AddField(
            model_name='userflow',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_history', to='template.shoptemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='userflow',
            name='richmenu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_history', to='richmenu.shoprichmenu'),
        ),
        migrations.AddField(
            model_name='userflow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_flow', to='user.lineuser'),
        ),
        migrations.AddField(
            model_name='userflow',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flow_history', to='template.shoptemplatevideo'),
        ),
        migrations.AddField(
            model_name='shopflowtimer',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_timer', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowtemplatereminder',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template_reminder', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowtemplatereminder',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template_reminder', to='template.shoptemplatecardtype'),
        ),
        migrations.AddField(
            model_name='shopflowtemplatereminder',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template_reminder', to='template.shoptemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='shopflowtemplatereminder',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template_reminder', to='template.shoptemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='shopflowtemplatereminder',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template_reminder', to='template.shoptemplatetext'),
        ),
        migrations.AddField(
            model_name='shopflowtemplatereminder',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template_reminder', to='template.shoptemplatevideo'),
        ),
        migrations.AddField(
            model_name='shopflowtemplate',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowtemplate',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template', to='template.shoptemplatecardtype'),
        ),
        migrations.AddField(
            model_name='shopflowtemplate',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template', to='template.shoptemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='shopflowtemplate',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template', to='template.shoptemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='shopflowtemplate',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template', to='template.shoptemplatetext'),
        ),
        migrations.AddField(
            model_name='shopflowtemplate',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_template', to='template.shoptemplatevideo'),
        ),
        migrations.AddField(
            model_name='shopflowtab',
            name='flow',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_tab', to='flow.shopflow'),
        ),
        migrations.AddField(
            model_name='shopflowstep',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_step', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowstep',
            name='tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_step', to='flow.shopflowtab'),
        ),
        migrations.AddField(
            model_name='shopflowschedule',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_schedule', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowrichmenu',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_rich_menu', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowrichmenu',
            name='rich_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_rich_menu', to='richmenu.shoprichmenu'),
        ),
        migrations.AddField(
            model_name='shopflowresult',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_result', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowitem',
            name='flow_tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_item', to='flow.shopflowtab'),
        ),
        migrations.AddField(
            model_name='shopflowconditionitem',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_condition_item', to='flow.shopflowcondition'),
        ),
        migrations.AddField(
            model_name='shopflowcondition',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_condition', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowactionreminder',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_reminder', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowactionreminder',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_reminder', to='template.shoptemplatecardtype'),
        ),
        migrations.AddField(
            model_name='shopflowactionreminder',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_reminder', to='template.shoptemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='shopflowactionreminder',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_reminder', to='template.shoptemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='shopflowactionreminder',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_reminder', to='template.shoptemplatetext'),
        ),
        migrations.AddField(
            model_name='shopflowactionreminder',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_reminder', to='template.shoptemplatevideo'),
        ),
        migrations.AddField(
            model_name='shopflowactionmessage',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_message', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflowactionmessage',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_message', to='template.shoptemplatecardtype'),
        ),
        migrations.AddField(
            model_name='shopflowactionmessage',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_message', to='template.shoptemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='shopflowactionmessage',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_message', to='template.shoptemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='shopflowactionmessage',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_message', to='template.shoptemplatetext'),
        ),
        migrations.AddField(
            model_name='shopflowactionmessage',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action_message', to='template.shoptemplatevideo'),
        ),
        migrations.AddField(
            model_name='shopflowaction',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action', to='flow.shopflowtab'),
        ),
        migrations.AddField(
            model_name='shopflowaction',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow_action', to='flow.shopflowitem'),
        ),
        migrations.AddField(
            model_name='shopflow',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow', to='sign.authcompany'),
        ),
        migrations.AddField(
            model_name='shopflow',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow', to='flow.companyflow'),
        ),
        migrations.AddField(
            model_name='shopflow',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_flow', to='sign.authshop'),
        ),
        migrations.AddField(
            model_name='headflowtimer',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_timer', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowtemplatereminder',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template_reminder', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowtemplatereminder',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_templaet_reminder', to='template.headtemplatecardtype'),
        ),
        migrations.AddField(
            model_name='headflowtemplatereminder',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template_reminder', to='template.headtemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='headflowtemplatereminder',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template_reminder', to='template.headtemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='headflowtemplatereminder',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template_reminder', to='template.headtemplatetext'),
        ),
        migrations.AddField(
            model_name='headflowtemplatereminder',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template_reminder', to='template.headtemplatevideo'),
        ),
        migrations.AddField(
            model_name='headflowtemplate',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowtemplate',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template', to='template.headtemplatecardtype'),
        ),
        migrations.AddField(
            model_name='headflowtemplate',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template', to='template.headtemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='headflowtemplate',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template', to='template.headtemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='headflowtemplate',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template', to='template.headtemplatetext'),
        ),
        migrations.AddField(
            model_name='headflowtemplate',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_template', to='template.headtemplatevideo'),
        ),
        migrations.AddField(
            model_name='headflowtab',
            name='flow',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_tab', to='flow.headflow'),
        ),
        migrations.AddField(
            model_name='headflowstep',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_step', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowstep',
            name='tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_step', to='flow.headflowtab'),
        ),
        migrations.AddField(
            model_name='headflowschedule',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_schedule', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowrichmenu',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_rich_menu', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowrichmenu',
            name='rich_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_rich_menu', to='richmenu.headrichmenu'),
        ),
        migrations.AddField(
            model_name='headflowresult',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_result', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowitem',
            name='flow_tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_item', to='flow.headflowtab'),
        ),
        migrations.AddField(
            model_name='headflowconditionitem',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_condition_item', to='flow.headflowcondition'),
        ),
        migrations.AddField(
            model_name='headflowcondition',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_condition', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowactionreminder',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_reminder', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowactionreminder',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_reminder', to='template.headtemplatecardtype'),
        ),
        migrations.AddField(
            model_name='headflowactionreminder',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_reminder', to='template.headtemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='headflowactionreminder',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_reminder', to='template.headtemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='headflowactionreminder',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_reminder', to='template.headtemplatetext'),
        ),
        migrations.AddField(
            model_name='headflowactionreminder',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_reminder', to='template.headtemplatevideo'),
        ),
        migrations.AddField(
            model_name='headflowactionmessage',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_message', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='headflowactionmessage',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_message', to='template.headtemplatecardtype'),
        ),
        migrations.AddField(
            model_name='headflowactionmessage',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_message', to='template.headtemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='headflowactionmessage',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_message', to='template.headtemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='headflowactionmessage',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_message', to='template.headtemplatetext'),
        ),
        migrations.AddField(
            model_name='headflowactionmessage',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action_message', to='template.headtemplatevideo'),
        ),
        migrations.AddField(
            model_name='headflowaction',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action', to='flow.headflowtab'),
        ),
        migrations.AddField(
            model_name='headflowaction',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_flow_action', to='flow.headflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowtimer',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_timer', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowtemplatereminder',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template_reminder', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowtemplatereminder',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template_reminder', to='template.companytemplatecardtype'),
        ),
        migrations.AddField(
            model_name='companyflowtemplatereminder',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template_reminder', to='template.companytemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='companyflowtemplatereminder',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template_reminder', to='template.companytemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='companyflowtemplatereminder',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template_reminder', to='template.companytemplatetext'),
        ),
        migrations.AddField(
            model_name='companyflowtemplatereminder',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template_reminder', to='template.companytemplatevideo'),
        ),
        migrations.AddField(
            model_name='companyflowtemplate',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowtemplate',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template', to='template.companytemplatecardtype'),
        ),
        migrations.AddField(
            model_name='companyflowtemplate',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template', to='template.companytemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='companyflowtemplate',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template', to='template.companytemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='companyflowtemplate',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template', to='template.companytemplatetext'),
        ),
        migrations.AddField(
            model_name='companyflowtemplate',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_template', to='template.companytemplatevideo'),
        ),
        migrations.AddField(
            model_name='companyflowtab',
            name='flow',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_tab', to='flow.companyflow'),
        ),
        migrations.AddField(
            model_name='companyflowstep',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_step', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowstep',
            name='tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_step', to='flow.companyflowtab'),
        ),
        migrations.AddField(
            model_name='companyflowschedule',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_schedule', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowrichmenu',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_rich_menu', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowrichmenu',
            name='rich_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_rich_menu', to='richmenu.companyrichmenu'),
        ),
        migrations.AddField(
            model_name='companyflowresult',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_result', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowitem',
            name='flow_tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_item', to='flow.companyflowtab'),
        ),
        migrations.AddField(
            model_name='companyflowconditionitem',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_condition_item', to='flow.companyflowcondition'),
        ),
        migrations.AddField(
            model_name='companyflowcondition',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_condition', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowactionreminder',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_reminder', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowactionreminder',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_reminder', to='template.companytemplatecardtype'),
        ),
        migrations.AddField(
            model_name='companyflowactionreminder',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_reminder', to='template.companytemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='companyflowactionreminder',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_reminder', to='template.companytemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='companyflowactionreminder',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_reminder', to='template.companytemplatetext'),
        ),
        migrations.AddField(
            model_name='companyflowactionreminder',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_reminder', to='template.companytemplatevideo'),
        ),
        migrations.AddField(
            model_name='companyflowactionmessage',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_message', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflowactionmessage',
            name='template_cardtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_message', to='template.companytemplatecardtype'),
        ),
        migrations.AddField(
            model_name='companyflowactionmessage',
            name='template_richmessage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_message', to='template.companytemplaterichmessage'),
        ),
        migrations.AddField(
            model_name='companyflowactionmessage',
            name='template_richvideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_message', to='template.companytemplaterichvideo'),
        ),
        migrations.AddField(
            model_name='companyflowactionmessage',
            name='template_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_message', to='template.companytemplatetext'),
        ),
        migrations.AddField(
            model_name='companyflowactionmessage',
            name='template_video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action_message', to='template.companytemplatevideo'),
        ),
        migrations.AddField(
            model_name='companyflowaction',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action', to='flow.companyflowtab'),
        ),
        migrations.AddField(
            model_name='companyflowaction',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_flow_action', to='flow.companyflowitem'),
        ),
        migrations.AddField(
            model_name='companyflow',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow', to='sign.authcompany'),
        ),
        migrations.AddField(
            model_name='companyflow',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_flow', to='flow.headflow'),
        ),
    ]
