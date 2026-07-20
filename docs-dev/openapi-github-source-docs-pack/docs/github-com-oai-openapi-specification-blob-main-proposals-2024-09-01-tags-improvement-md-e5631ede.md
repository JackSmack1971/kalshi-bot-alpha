---
title: "2024-09-01-Tags-Improvement.md"
source_url: "https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md"
host: "github.com"
depth: 2
selector: "markdown-native"
fetched_at: "2026-07-17T17:42:59.819Z"
---
<!DOCTYPE html>
<html
  lang="en"

  data-color-mode="auto" data-light-theme="light" data-dark-theme="dark"
  data-a11y-animated-images="system" data-a11y-link-underlines="true"

  >


  <head>
    <meta charset="utf-8">
  <link rel="dns-prefetch" href="https://github.githubassets.com">
  <link rel="dns-prefetch" href="https://avatars.githubusercontent.com">
  <link rel="dns-prefetch" href="https://github-cloud.s3.amazonaws.com">
  <link rel="dns-prefetch" href="https://user-images.githubusercontent.com/">
  <link rel="preconnect" href="https://github.githubassets.com" crossorigin>
  <link rel="preconnect" href="https://avatars.githubusercontent.com">


  <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/light-62b06818b06b09b7.css" /><link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/light_high_contrast-44cd405df9340c5c.css" /><link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/dark-f3311053b052c5d4.css" /><link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/dark_high_contrast-6739a26cef6aaf8e.css" /><link data-color-theme="light" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/light-62b06818b06b09b7.css" /><link data-color-theme="light_high_contrast" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/light_high_contrast-44cd405df9340c5c.css" /><link data-color-theme="light_colorblind" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/light_colorblind-646991fe4831aa4c.css" /><link data-color-theme="light_colorblind_high_contrast" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/light_colorblind_high_contrast-4a10ec40fc7845a6.css" /><link data-color-theme="light_tritanopia" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/light_tritanopia-ad55fa69f5aaa75d.css" /><link data-color-theme="light_tritanopia_high_contrast" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/light_tritanopia_high_contrast-eed7315d90377f7a.css" /><link data-color-theme="dark" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark-f3311053b052c5d4.css" /><link data-color-theme="dark_high_contrast" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_high_contrast-6739a26cef6aaf8e.css" /><link data-color-theme="dark_colorblind" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_colorblind-46654068ac8d8b19.css" /><link data-color-theme="dark_colorblind_high_contrast" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_colorblind_high_contrast-ce6091c5adfeb70f.css" /><link data-color-theme="dark_tritanopia" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_tritanopia-a1584556afb3c856.css" /><link data-color-theme="dark_tritanopia_high_contrast" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_tritanopia_high_contrast-f48b2521c34c41b6.css" /><link data-color-theme="dark_dimmed" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_dimmed-6199d2c64677af2d.css" /><link data-color-theme="dark_dimmed_high_contrast" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_dimmed_high_contrast-a8e662a03107fa71.css" />

  <style type="text/css">
    :root {
      --tab-size-preference: 4;
    }

    pre, code {
      tab-size: var(--tab-size-preference);
    }
  </style>

    <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/primer-primitives-ac2f4b33720c6312.css" />
    <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/primer-bb3e7caff8347285.css" />
    <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/global-e7276ff9ba0dc008.css" />
    <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/github-9feca2dee6fea037.css" />
  <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/repository-6534fbc3f5e83ac0.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/code-2e8b2d0c3572ac0b.css" />


  <script type="application/json" id="client-env">{"locale":"en","featureFlags":["actions_custom_images_storage_billing_ui_visibility","actions_enable_background_steps","actions_image_version_event","agent_author_search_expansion","agent_author_search_expansion_ui_pulls","alternate_user_config_repo","artifact_ui_v2","billing_billable_licenses_cost_center_bucket_fix","billing_cost_center_user_level_budgets","billing_discount_threshold_notification","billing_multi_user_cost_center_total_user_count","billing_user_level_budgets","billing_user_level_budgets_manage","code_quality_new_repo_selection_card","code_scanning_dfa_degraded_experience_notice","code_view_raf_sticky_lines","codespaces_prebuild_region_target_update","coding_agent_third_party_model_ui","comment_viewer_copy_raw_markdown","contentful_primer_code_blocks","copilot_agent_snippy","copilot_api_agentic_issue_marshal_yaml","copilot_ask_mode_dropdown","copilot_automations_pagination","copilot_chat_attach_multiple_images","copilot_chat_auto_mode_picker_paid","copilot_chat_category_rate_limit_messages","copilot_chat_clear_model_selection_for_default_change","copilot_chat_compact_tables","copilot_chat_contextual_suggestions_updated","copilot_chat_docked_panel","copilot_chat_enable_tool_call_logs","copilot_chat_fix_fallback_auto_discount","copilot_chat_input_commands","copilot_chat_interspersed_tool_calls","copilot_chat_max_upsell","copilot_chat_model_picker_info_popover","copilot_chat_models_browser_cache","copilot_chat_opening_thread_switch","copilot_chat_per_message_token_usage","copilot_chat_prettify_pasted_code","copilot_chat_reduce_quota_checks","copilot_chat_ubb_meter","copilot_chat_vision_dotcom_chat_ga_gate","copilot_chat_vision_in_claude","copilot_chat_vision_preview_gate","copilot_cli_install_cta_max_plan","copilot_css_textarea_autosize","copilot_custom_copilots","copilot_custom_copilots_feature_preview","copilot_diff_explain_conversation_intent","copilot_diff_reference_context","copilot_duplicate_thread","copilot_extensions_removal_on_marketplace","copilot_file_block_ref_matching","copilot_fix_failed_workflows","copilot_fix_failed_workflows_all_skus","copilot_ftp_hyperspace_upgrade_prompt","copilot_hide_hovercard","copilot_immersive_code_block_transition_wrap","copilot_immersive_embedded_deferred_payload","copilot_immersive_embedded_draggable","copilot_immersive_embedded_header_button","copilot_immersive_embedded_implicit_references","copilot_immersive_embedded_skip_copilot_api_token_for_dotcom_context","copilot_immersive_file_block_transition_open","copilot_immersive_file_preview_keep_mounted","copilot_immersive_job_result_preview","copilot_immersive_suggestion_pills","copilot_immersive_task_hyperlinking","copilot_immersive_task_within_chat_thread","copilot_mc_cli_resume_any_users_task","copilot_mc_nudges","copilot_mission_control_agent_filtering","copilot_mission_control_environment_list_icons","copilot_mission_control_initial_data_spinner","copilot_mission_control_needs_attention","copilot_mission_control_sandbox_remote_bypass","copilot_mission_control_session_events_ui","copilot_mission_control_session_filters","copilot_mission_control_task_alive_updates","copilot_mission_control_task_sharing","copilot_org_policy_page_focus_mode","copilot_plans_signups_enabled","copilot_pr_chat_enhancements","copilot_prominent_upgrade_button","copilot_redirect_header_button_to_agents","copilot_resource_panel","copilot_share_active_subthread","copilot_spaces_ga","copilot_spaces_individual_policies_ga","copilot_spark_empty_state","copilot_spark_handle_nil_friendly_name","copilot_swe_agent_authorization_status_ui","copilot_swe_agent_hide_model_picker_if_only_auto","copilot_swe_agent_issue_comment_trigger","copilot_swe_agent_pr_comment_model_picker","copilot_swe_agent_pull_request_comment_trigger","copilot_swe_agent_pull_request_merged_trigger","copilot_swe_agent_pull_request_opened_trigger","copilot_swe_agent_pull_request_synchronize_trigger","copilot_swe_agent_use_subagents","copilot_task_api_github_rest_style","copilot_token_based_billing","copilot_unconfigured_is_inherited","copilot_user_can_upgrade_plan_field","copilot_workbench_ubb","dashboard_indexeddb_caching","dashboard_lists_max_age_filter","dashboard_surface_persistent_preferences","dashboard_universe_2025_feedback_dialog","flex_cta_groups_mvp","ga_enterprise_teams_ui","global_nav_react","hyperspace_2025_logged_out_batch_1","hyperspace_2025_logged_out_batch_2","hyperspace_2025_logged_out_batch_3","in_product_messaging_datadog_monitoring","ipm_budget_deep_linking","ipm_global_transactional_message_agents","ipm_global_transactional_message_copilot","ipm_global_transactional_message_issues","ipm_global_transactional_message_prs","ipm_global_transactional_message_repos","ipm_global_transactional_message_spaces","issue_cca_modal_open","issue_cca_multi_assign_modal","issue_cca_visualization","issue_fields_global_search","issue_fields_index_pills","issue_inline_avatars","issue_relative_time_micro","issues_expanded_file_types","issues_lazy_load_comment_box_suggestions","issues_react_chrome_container_query_fix","landing_pages_ninetailed","landing_pages_web_vitals_tracking","lifecycle_label_name_updates","low_quality_classifier","marketing_pages_search_explore_provider","memex_default_issue_create_repository","memex_lazy_hydrate_agent_tasks","memex_live_update_hovercard","memex_mwl_filter_field_delimiter","memex_remove_deprecated_type_issue","merge_status_header_feedback","oauth_authorize_clickjacking_protection","octocaptcha_origin_optimization","primer_react_css_anchor_positioning","property_definition_empty_state_suggestions","prs_copilot_app_open_action","prs_css_anchor_positioning","pull_request_copilot_attribution_header","react_blob_isolate_code_lines","react_data_router_tanstack_allowed","react_router_external_route_handoff","react_sandbox_future_tanstack","repo_issues_sidebar_layout","repo_overview_ask_copilot","repos_contributors_limited_default_range","review_involves_filter","rules_insights_filter_bar_created","sample_network_conn_type","secret_scanning_pattern_alerts_link","security_center_artifact_filters_popover","semantic_similarity_duplicate_issue_detection","session_logs_ungroup_reasoning_text","site_banner_desktop_copilot_app","site_github_app_ga_page","site_global_banner_learn_copilot_app","site_global_banner_security_webinar","site_global_nav_spark_models_removed","spark_prompt_secret_scanning","spark_server_connection_status","suppress_automated_browser_vitals","swp_forms_disable_octocaptcha","universe26_banners_seblaunch","viewscreen_sandbox","warn_inaccessible_attachments","webp_support","workbench_store_readonly"],"copilotApiOverrideUrl":"https://api.githubcopilot.com","cmcApiUrl":"https://api.github.com/cmc_internal/api"}</script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/high-contrast-cookie-e99d8801a8e707d0.js"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/wp-runtime-8e17fb290f6af116.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/app-foundation-1148b3375bce34af.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/app-runtime-ef0dc254e0d9303a.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/fetch-utilities-2806a89cc961108e.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/78205-5d6a6f402b7a8e68.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/89415-812392e4104ab411.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/environment-f3f12838044fcdcf.js" defer="defer"></script>
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/app-runtime.5ac1c30bfb20c312.module.css" />
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/runtime-helpers-07d9b6c19e17ed0e.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/catalyst-2b159a120cac7df3.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/selector-observer-6cc59d6d6cb4ac45.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/relative-time-element-53f90fd67c911d95.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/296-4c0a68ac3f1b71d1.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/816-8d95115b2deb6077.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/21265-6a76b64e3534ad57.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/81683-bbf17e7ded27669b.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/46740-eafd9231dd2851b5.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/30058-a587bf91d659fae4.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/github-elements-9c0e90e6da2c718a.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/element-registry-64f2f927394664a8.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/aria-live-e19e787d92ce5691.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/hotkey-1338be440a91805c.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/react-core-779aa9beee262780.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/react-lib-8374452cf670a3dd.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/38566-18d0a37605b397b1.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/79039-f3a5d669cf7dafb8.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/88475-b108bff2e4d2f3b9.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/26533-40828ca3a25cd387.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/3092-3835ccf9e736f8f3.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/62870-e1debc71677344a3.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/85720-4d25c178319d3929.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/74294-37a7fce1f35f232b.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/29863-ab3f485fdc17575f.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/27956-b37ebf88845b377c.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/24061-924c3ecefbdc3dc8.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/behaviors-f32f625151c0f83c.js" defer="defer"></script>
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/react-core.41d235956ab401f9.module.css" />
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/notifications-global-e88c9edde27b90c3.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/94128-2283bb00fc03e74a.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/code-menu-00b724bcbb8fa494.js" defer="defer"></script>

  <script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/primer-react-98420ac0b3a270da.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/octicons-react-18b2c0cd5494100e.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/65063-bd8203e1dd0b89c0.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/437-419907f8f35fdea5.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/41328-58fd5c991cf22249.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/7463-c53cb51bb7bcb6c4.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/27600-0e4c25b9966aa15b.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/88493-9ebec306434f2746.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/47406-d23036dd6c1f8b99.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/76041-a6f3ef7ba2d359b5.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/27784-0112a594e916e721.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/99829-9afc122ab8cee792.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/71192-4386a645531b5440.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/4871-f3fe244d12d50c8e.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/12540-c842828ab3aa4d1a.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/57664-8edaaf8dbbdda224.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/56324-8a8fbd03a34663cd.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/4706-45d3000d5efad6d2.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/47278-d9078a730c8958f1.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/1966-fbfbfc822eb8550d.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/8151-2036b4a45274e8b5.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/10257-c2d9ec71122a1668.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/11494-cf7adebd00e07dc8.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/13735-09a704d2a440246b.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/99788-0f158acfb8fdecf1.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/30223-ef4189dbba91230c.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/21472-af577251473db06d.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/79589-eaeae7c41418eaba.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/24860-de80870afe0fc78a.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/85736-d9caa530f35ccac2.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/15119-0ddc41fa627323a4.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/62192-fafe1486852c14a1.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/64029-54237272397eb3b1.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/66917-4586116605ec45e8.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/3399-7a46a2831d60fcd9.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/26473-c7af40bc9bfc724a.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/4409-0c0b8a0ad1c062d9.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/code-view-fcd019b905a2cbe4.js" defer="defer"></script>
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/primer-react-css.244a979f6c5947c6.module.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/99788.7be3864135368ac9.module.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/4409.78baa976c45ac386.module.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/code-view.32a1aaaabb55dea2.module.css" />

  <script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/93986-f4c7538bab703c72.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/22415-197e1f8b4709a7cd.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/notifications-subscriptions-menu-6e5771b2954ed583.js" defer="defer"></script>
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/primer-react-css.244a979f6c5947c6.module.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/notifications-subscriptions-menu.9cd46ccda9f59c29.module.css" />


  <title>OpenAPI-Specification/proposals/2024-09-01-Tags-Improvement.md at main · OAI/OpenAPI-Specification · GitHub</title>


  <meta name="route-pattern" content="/:user_id/:repository/blob/*name(/*path)" data-turbo-transient>
  <meta name="route-controller" content="blob" data-turbo-transient>
  <meta name="route-action" content="show" data-turbo-transient>
  <meta name="fetch-nonce" content="v2:e9423f9d-26fb-4cea-5439-647b0434eaa0">


  <meta name="current-catalog-service-hash" content="f3abb0cc802f3d7b95fc8762b94bdcb13bf39634c40c357301c4aa1d67a256fb">


  <meta name="request-id" content="4002:1DD20D:181FA5:20D8EB:6A5A69A3" data-pjax-transient="true"/><meta name="html-safe-nonce" content="37994ae92d4964a454caacf1ff260a443a2adfcc1b0e109e9548f5de17cc6cc2" data-pjax-transient="true"/><meta name="visitor-payload" content="eyJyZWZlcnJlciI6IiIsInJlcXVlc3RfaWQiOiI0MDAyOjFERDIwRDoxODFGQTU6MjBEOEVCOjZBNUE2OUEzIiwidmlzaXRvcl9pZCI6IjY4NjA2MDM1Mjg1ODkyNDA3MzkiLCJyZWdpb25fZWRnZSI6ImlhZCIsInJlZ2lvbl9yZW5kZXIiOiJpYWQifQ==" data-pjax-transient="true"/><meta name="visitor-hmac" content="2df4b2e20cc1c9afc5e4557acb2a004f985e3c6af930ed2a78047dfe5804662f" data-pjax-transient="true"/>


    <meta name="hovercard-subject-tag" content="repository:17372733" data-turbo-transient>


  <meta name="github-keyboard-shortcuts" content="repository,source-code,file-tree,copilot" data-turbo-transient="true" />


  <meta name="selected-link" value="repo_source" data-turbo-transient>
  <link rel="assets" href="https://github.githubassets.com/">

    <meta name="google-site-verification" content="Apib7-x98H0j5cPqHWwSMm6dNU4GmODRoqxLiDzdx9I">

<meta name="octolytics-url" content="https://collector.github.com/github/collect" />


  <meta name="analytics-location" content="/&lt;user-name&gt;/&lt;repo-name&gt;/blob/show" data-turbo-transient="true" />


    <meta name="user-login" content="">


    <meta name="viewport" content="width=device-width">


      <meta name="description" content="The OpenAPI Specification Repository. Contribute to OAI/OpenAPI-Specification development by creating an account on GitHub.">

      <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">

    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <meta property="fb:app_id" content="1401488693436528">
    <meta name="apple-itunes-app" content="app-id=1477376905, app-argument=https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md" />

      <meta name="twitter:image" content="https://opengraph.githubassets.com/c42ca48e7d20faada40581dc4b9ee499f1a72cf74060d0741a552174a07bf4a2/OAI/OpenAPI-Specification" /><meta name="twitter:site" content="@github" /><meta name="twitter:card" content="summary_large_image" /><meta name="twitter:title" content="OpenAPI-Specification/proposals/2024-09-01-Tags-Improvement.md at main · OAI/OpenAPI-Specification" /><meta name="twitter:description" content="The OpenAPI Specification Repository. Contribute to OAI/OpenAPI-Specification development by creating an account on GitHub." />
  <meta property="og:image" content="https://opengraph.githubassets.com/c42ca48e7d20faada40581dc4b9ee499f1a72cf74060d0741a552174a07bf4a2/OAI/OpenAPI-Specification" /><meta property="og:image:alt" content="The OpenAPI Specification Repository. Contribute to OAI/OpenAPI-Specification development by creating an account on GitHub." /><meta property="og:image:width" content="1200" /><meta property="og:image:height" content="600" /><meta property="og:site_name" content="GitHub" /><meta property="og:type" content="object" /><meta property="og:title" content="OpenAPI-Specification/proposals/2024-09-01-Tags-Improvement.md at main · OAI/OpenAPI-Specification" /><meta property="og:url" content="https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md" /><meta property="og:description" content="The OpenAPI Specification Repository. Contribute to OAI/OpenAPI-Specification development by creating an account on GitHub." />


      <meta name="hostname" content="github.com">


        <meta name="expected-hostname" content="github.com">


  <meta http-equiv="x-pjax-version" content="ce5c9035b773a59b90caca02283126458f561eff6d79864e0c214618d317426b" data-turbo-track="reload">
  <meta http-equiv="x-pjax-csp-version" content="cb4cffb7c023f774818cf728eb860debf1fc8ecf88a20487b238da276df1eb7d" data-turbo-track="reload">
  <meta http-equiv="x-pjax-css-version" content="2988e48440351883d0da1600d97518db97f8352e46a1073cf64cc42ac1ff44b4" data-turbo-track="reload">
  <meta http-equiv="x-pjax-js-version" content="922bdba685ea48400234d557977f0e32d9adbae6f5125725b4f48cacc6801106" data-turbo-track="reload">

  <meta name="turbo-cache-control" content="no-preview" data-turbo-transient="">

      <meta name="turbo-cache-control" content="no-cache" data-turbo-transient>

    <meta data-hydrostats="publish">

  <meta name="go-import" content="github.com/OAI/OpenAPI-Specification git https://github.com/OAI/OpenAPI-Specification.git">

  <meta name="octolytics-dimension-user_id" content="16343502" /><meta name="octolytics-dimension-user_login" content="OAI" /><meta name="octolytics-dimension-repository_id" content="17372733" /><meta name="octolytics-dimension-repository_nwo" content="OAI/OpenAPI-Specification" /><meta name="octolytics-dimension-repository_public" content="true" /><meta name="octolytics-dimension-repository_is_fork" content="false" /><meta name="octolytics-dimension-repository_network_root_id" content="17372733" /><meta name="octolytics-dimension-repository_network_root_nwo" content="OAI/OpenAPI-Specification" />


    <meta name="turbo-body-classes" content="logged-out env-production page-responsive">
  <meta name="disable-turbo" content="false">


  <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">


  <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">

    <meta name="release" content="03575fc589c0e2692de839d7ca2b3aa5b5179f52" data-turbo-track="reload">
  <meta name="ui-target" content="full">

  <link rel="mask-icon" href="https://github.githubassets.com/assets/pinned-octocat-093da3e6fa40.svg" color="#000000">
  <link rel="alternate icon" class="js-site-favicon" type="image/png" href="https://github.githubassets.com/favicons/favicon.png">
  <link rel="icon" class="js-site-favicon" type="image/svg+xml" href="https://github.githubassets.com/favicons/favicon.svg" data-base-href="https://github.githubassets.com/favicons/favicon">

<meta name="theme-color" content="#1e2327">
<meta name="color-scheme" content="light dark" />


  <link rel="manifest" href="/manifest.json" crossOrigin="use-credentials">

  </head>

  <body class="logged-out env-production page-responsive" style="word-wrap: break-word;" >
    <div data-turbo-body class="logged-out env-production page-responsive" style="word-wrap: break-word;" >
      <div id="__primerPortalRoot__" style="z-index: 1000; position: absolute; width: 100%;" data-turbo-permanent></div>


    <div class="position-relative header-wrapper js-header-wrapper ">
      <a href="#start-of-content" data-skip-target-assigned="false" class="px-2 tmp-py-4 color-bg-accent-emphasis color-fg-on-emphasis show-on-focus js-skip-to-content">Skip to content</a>

      <span data-view-component="true" class="progress-pjax-loader Progress position-fixed width-full">
    <span style="width: 0%;" data-view-component="true" class="Progress-item progress-pjax-loader-bar left-0 top-0 color-bg-accent-emphasis"></span>
</span>
      <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/primer-react-css.244a979f6c5947c6.module.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/keyboard-shortcuts-dialog.7d5cc9abd7aa8f78.module.css" />

<react-partial
  partial-name="keyboard-shortcuts-dialog"
  data-ssr="false"
  data-attempted-ssr="false"
  data-react-profiling="false"
>

  <script type="application/json" data-target="react-partial.embeddedData">{"props":{"docsUrl":"https://docs.github.com/get-started/accessibility/keyboard-shortcuts"}}</script>
  <div data-target="react-partial.reactRoot"></div>
</react-partial>


<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/70666-2f0147a238106a53.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/80137-34ca1387246c1434.js" defer="defer"></script>
<script crossorigin="anonymous" type="module" src="https://github.githubassets.com/assets/sessions-ecd48f3a76a81b14.js" defer="defer"></script>

<style>
  /* Override primer focus outline color for marketing header dropdown links for better contrast */
  [data-color-mode="light"] .HeaderMenu-dropdown-link:focus-visible,
  [data-color-mode="light"] .HeaderMenu-trailing-link a:focus-visible {
    outline-color: var(--color-accent-fg);
  }
</style>

<header class="HeaderMktg header-logged-out js-details-container js-header Details f4 tmp-py-3" role="banner" data-is-top="true" data-color-mode=auto data-light-theme=light data-dark-theme=dark>
  <h2 class="sr-only">Navigation Menu</h2>

  <button type="button" class="HeaderMktg-backdrop d-lg-none border-0 position-fixed top-0 left-0 width-full height-full js-details-target" aria-label="Toggle navigation">
    <span class="d-none">Toggle navigation</span>
  </button>

  <div class="d-flex flex-column flex-lg-row flex-items-center tmp-px-3 tmp-px-md-4 tmp-px-lg-5 height-full position-relative z-1">
    <div class="d-flex flex-justify-between flex-items-center width-full width-lg-auto">
      <div class="flex-1">
        <button aria-label="Toggle navigation" aria-expanded="false" type="button" data-view-component="true" class="js-details-target js-nav-padding-recalculate js-header-menu-toggle Button--link Button--medium Button d-lg-none color-fg-inherit p-1 tmp-p-1">  <span class="Button-content">
    <span class="Button-label"><div class="HeaderMenu-toggle-bar rounded my-1"></div>
            <div class="HeaderMenu-toggle-bar rounded my-1"></div>
            <div class="HeaderMenu-toggle-bar rounded my-1"></div></span>
  </span>
</button>
      </div>

      <a class="tmp-mr-lg-3 color-fg-inherit flex-order-2 js-prevent-focus-on-mobile-nav"
        href="/"
        aria-label="Homepage"
        data-analytics-event="{&quot;category&quot;:&quot;Marketing nav&quot;,&quot;action&quot;:&quot;click to go to homepage&quot;,&quot;label&quot;:&quot;ref_page:Marketing;ref_cta:Logomark;ref_loc:Header&quot;}">
        <svg height="32" aria-hidden="true" data-component="Octicon" viewBox="0 0 24 24" version="1.1" width="32" data-view-component="true" class="octicon octicon-mark-github">
    <path d="M10.226 17.284c-2.965-.36-5.054-2.493-5.054-5.256 0-1.123.404-2.336 1.078-3.144-.292-.741-.247-2.314.09-2.965.898-.112 2.111.36 2.83 1.01.853-.269 1.752-.404 2.853-.404 1.1 0 1.999.135 2.807.382.696-.629 1.932-1.1 2.83-.988.315.606.36 2.179.067 2.942.72.854 1.101 2 1.101 3.167 0 2.763-2.089 4.852-5.098 5.234.763.494 1.28 1.572 1.28 2.807v2.336c0 .674.561 1.056 1.235.786 4.066-1.55 7.255-5.615 7.255-10.646C23.5 6.188 18.334 1 11.978 1 5.62 1 .5 6.188.5 12.545c0 4.986 3.167 9.12 7.435 10.669.606.225 1.19-.18 1.19-.786V20.63a2.9 2.9 0 0 1-1.078.224c-1.483 0-2.359-.808-2.987-2.313-.247-.607-.517-.966-1.034-1.033-.27-.023-.359-.135-.359-.27 0-.27.45-.471.898-.471.652 0 1.213.404 1.797 1.235.45.651.921.943 1.483.943.561 0 .92-.202 1.437-.719.382-.381.674-.718.944-.943"></path>
</svg>
      </a>

      <div class="d-flex flex-1 flex-order-2 text-right d-lg-none gap-2 flex-justify-end">
          <a
            href="/login?return_to=https%3A%2F%2Fgithub.com%2FOAI%2FOpenAPI-Specification%2Fblob%2Fmain%2Fproposals%2F2024-09-01-Tags-Improvement.md"
            class="HeaderMenu-link HeaderMenu-button d-inline-flex f5 no-underline border color-border-default rounded-2 px-2 py-1 color-fg-inherit js-prevent-focus-on-mobile-nav"
            data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;site header menu&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;SIGN_UP&quot;,&quot;originating_url&quot;:&quot;https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="580c046b2ad1df6bcec88f2fb8ee58ccf0a077fc269a350f45137aaae2ec3e9e"
            data-analytics-event="{&quot;category&quot;:&quot;Marketing nav&quot;,&quot;action&quot;:&quot;click to Sign in&quot;,&quot;label&quot;:&quot;ref_page:Marketing;ref_cta:Sign in;ref_loc:Header&quot;}"
          >
            Sign in
          </a>
              <div class="AppHeader-appearanceSettings">
    <react-partial-anchor>
      <button data-target="react-partial-anchor.anchor" id="icon-button-68485730-b080-4b23-b614-d411faa78e03" aria-labelledby="tooltip-8f47b7ee-7dff-4dfe-bb5c-8a30351783b7" type="button" disabled="disabled" data-view-component="true" class="Button Button--iconOnly Button--invisible Button--medium AppHeader-button HeaderMenu-link border cursor-wait">  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-sliders Button-visual">
    <path d="M15 2.75a.75.75 0 0 1-.75.75h-4a.75.75 0 0 1 0-1.5h4a.75.75 0 0 1 .75.75Zm-8.5.75v1.25a.75.75 0 0 0 1.5 0v-4a.75.75 0 0 0-1.5 0V2H1.75a.75.75 0 0 0 0 1.5H6.5Zm1.25 5.25a.75.75 0 0 0 0-1.5h-6a.75.75 0 0 0 0 1.5h6ZM15 8a.75.75 0 0 1-.75.75H11.5V10a.75.75 0 1 1-1.5 0V6a.75.75 0 0 1 1.5 0v1.25h2.75A.75.75 0 0 1 15 8Zm-9 5.25v-2a.75.75 0 0 0-1.5 0v1.25H1.75a.75.75 0 0 0 0 1.5H4.5v1.25a.75.75 0 0 0 1.5 0v-2Zm9 0a.75.75 0 0 1-.75.75h-6a.75.75 0 0 1 0-1.5h6a.75.75 0 0 1 .75.75Z"></path>
</svg>
</button><tool-tip id="tooltip-8f47b7ee-7dff-4dfe-bb5c-8a30351783b7" for="icon-button-68485730-b080-4b23-b614-d411faa78e03" popover="manual" data-direction="s" data-type="label" data-view-component="true" class="sr-only position-absolute">Appearance settings</tool-tip>

      <template data-target="react-partial-anchor.template">
        <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/primer-react-css.244a979f6c5947c6.module.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/appearance-settings.689ddb386a317f55.module.css" />

<react-partial
  partial-name="appearance-settings"
  data-ssr="false"
  data-attempted-ssr="false"
  data-react-profiling="false"
>

  <script type="application/json" data-target="react-partial.embeddedData">{"props":{}}</script>
  <div data-target="react-partial.reactRoot"></div>
</react-partial>


      </template>
    </react-partial-anchor>
  </div>

      </div>
    </div>


    <div class="HeaderMenu js-header-menu height-fit position-lg-relative d-lg-flex flex-column flex-auto top-0">
      <div class="HeaderMenu-wrapper d-flex flex-column flex-self-start flex-lg-row flex-auto rounded rounded-lg-0">
          <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/primer-react-css.244a979f6c5947c6.module.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/marketing-navigation.7da818c31d024167.module.css" />

<react-partial
  partial-name="marketing-navigation"
  data-ssr="true"
  data-attempted-ssr="true"
  data-react-profiling="false"
>

  <script type="application/json" data-target="react-partial.embeddedData">{"props":{"should_use_dotcom_links":true}}</script>
  <div data-target="react-partial.reactRoot"><nav class="MarketingNavigation-module__nav__W0KYY" aria-label="Global"><ul class="MarketingNavigation-module__list__tFbMb"><li><div class="NavDropdown-module__container__l2YeI js-details-container js-header-menu-item"><button type="button" class="NavDropdown-module__button__PEHWX js-details-target" aria-expanded="false">Platform<svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavDropdown-module__buttonIcon__Tkl8_" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></button><div class="NavDropdown-module__dropdown__xm1jd"><ul class="NavDropdown-module__list__zuCgG"><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_m5_">AI CODE CREATION</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_m5_"><li><a href="https://github.com/features/copilot" data-analytics-event="{&quot;action&quot;:&quot;github_copilot&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;github_copilot_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-copilot NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M23.922 16.992c-.861 1.495-5.859 5.023-11.922 5.023-6.063 0-11.061-3.528-11.922-5.023A.641.641 0 0 1 0 16.736v-2.869a.841.841 0 0 1 .053-.22c.372-.935 1.347-2.292 2.605-2.656.167-.429.414-1.055.644-1.517a10.195 10.195 0 0 1-.052-1.086c0-1.331.282-2.499 1.132-3.368.397-.406.89-.717 1.474-.952 1.399-1.136 3.392-2.093 6.122-2.093 2.731 0 4.767.957 6.166 2.093.584.235 1.077.546 1.474.952.85.869 1.132 2.037 1.132 3.368 0 .368-.014.733-.052 1.086.23.462.477 1.088.644 1.517 1.258.364 2.233 1.721 2.605 2.656a.832.832 0 0 1 .053.22v2.869a.641.641 0 0 1-.078.256ZM12.172 11h-.344a4.323 4.323 0 0 1-.355.508C10.703 12.455 9.555 13 7.965 13c-1.725 0-2.989-.359-3.782-1.259a2.005 2.005 0 0 1-.085-.104L4 11.741v6.585c1.435.779 4.514 2.179 8 2.179 3.486 0 6.565-1.4 8-2.179v-6.585l-.098-.104s-.033.045-.085.104c-.793.9-2.057 1.259-3.782 1.259-1.59 0-2.738-.545-3.508-1.492a4.323 4.323 0 0 1-.355-.508h-.016.016Zm.641-2.935c.136 1.057.403 1.913.878 2.497.442.544 1.134.938 2.344.938 1.573 0 2.292-.337 2.657-.751.384-.435.558-1.15.558-2.361 0-1.14-.243-1.847-.705-2.319-.477-.488-1.319-.862-2.824-1.025-1.487-.161-2.192.138-2.533.529-.269.307-.437.808-.438 1.578v.021c0 .265.021.562.063.893Zm-1.626 0c.042-.331.063-.628.063-.894v-.02c-.001-.77-.169-1.271-.438-1.578-.341-.391-1.046-.69-2.533-.529-1.505.163-2.347.537-2.824 1.025-.462.472-.705 1.179-.705 2.319 0 1.211.175 1.926.558 2.361.365.414 1.084.751 2.657.751 1.21 0 1.902-.394 2.344-.938.475-.584.742-1.44.878-2.497Z"></path><path d="M14.5 14.25a1 1 0 0 1 1 1v2a1 1 0 0 1-2 0v-2a1 1 0 0 1 1-1Zm-5 0a1 1 0 0 1 1 1v2a1 1 0 0 1-2 0v-2a1 1 0 0 1 1-1Z"></path></svg><span class="NavLink-module__title__Q7t0p">GitHub Copilot</span><span class="NavLink-module__subtitle__X4gkW">Write better code with AI</span></div></a></li><li><a href="https://github.com/features/ai/github-app" data-analytics-event="{&quot;action&quot;:&quot;github_copilot_app&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;github_copilot_app_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-mark-github NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M10.226 17.284c-2.965-.36-5.054-2.493-5.054-5.256 0-1.123.404-2.336 1.078-3.144-.292-.741-.247-2.314.09-2.965.898-.112 2.111.36 2.83 1.01.853-.269 1.752-.404 2.853-.404 1.1 0 1.999.135 2.807.382.696-.629 1.932-1.1 2.83-.988.315.606.36 2.179.067 2.942.72.854 1.101 2 1.101 3.167 0 2.763-2.089 4.852-5.098 5.234.763.494 1.28 1.572 1.28 2.807v2.336c0 .674.561 1.056 1.235.786 4.066-1.55 7.255-5.615 7.255-10.646C23.5 6.188 18.334 1 11.978 1 5.62 1 .5 6.188.5 12.545c0 4.986 3.167 9.12 7.435 10.669.606.225 1.19-.18 1.19-.786V20.63a2.9 2.9 0 0 1-1.078.224c-1.483 0-2.359-.808-2.987-2.313-.247-.607-.517-.966-1.034-1.033-.27-.023-.359-.135-.359-.27 0-.27.45-.471.898-.471.652 0 1.213.404 1.797 1.235.45.651.921.943 1.483.943.561 0 .92-.202 1.437-.719.382-.381.674-.718.944-.943"></path></svg><span class="NavLink-module__title__Q7t0p">GitHub Copilot app</span><span class="NavLink-module__subtitle__X4gkW">Direct agents from issue to merge</span></div></a></li><li><a href="https://github.com/mcp" data-analytics-event="{&quot;action&quot;:&quot;mcp_registry&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;mcp_registry_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-mcp NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M9.795 1.694a4.287 4.287 0 0 1 6.061 0 4.28 4.28 0 0 1 1.181 3.819 4.282 4.282 0 0 1 3.819 1.181 4.287 4.287 0 0 1 0 6.061l-6.793 6.793a.249.249 0 0 0 0 .353l2.617 2.618a.75.75 0 1 1-1.061 1.061l-2.617-2.618a1.75 1.75 0 0 1 0-2.475l6.793-6.793a2.785 2.785 0 1 0-3.939-3.939l-5.9 5.9a.734.734 0 0 1-.249.165.749.749 0 0 1-.812-1.225l5.9-5.901a2.785 2.785 0 1 0-3.939-3.939L2.931 10.68A.75.75 0 1 1 1.87 9.619l7.925-7.925Z"></path><path d="M12.42 4.069a.752.752 0 0 1 1.061 0 .752.752 0 0 1 0 1.061L7.33 11.28a2.788 2.788 0 0 0 0 3.94 2.788 2.788 0 0 0 3.94 0l6.15-6.151a.752.752 0 0 1 1.061 0 .752.752 0 0 1 0 1.061l-6.151 6.15a4.285 4.285 0 1 1-6.06-6.06l6.15-6.151Z"></path></svg><span class="NavLink-module__title__Q7t0p">MCP Registry<sup class="NavLink-module__label__bil7n">New</sup></span><span class="NavLink-module__subtitle__X4gkW">Integrate external tools</span></div></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_165_">DEVELOPER WORKFLOWS</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_165_"><li><a href="https://github.com/features/actions" data-analytics-event="{&quot;action&quot;:&quot;actions&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;actions_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-workflow NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M1 3a2 2 0 0 1 2-2h6.5a2 2 0 0 1 2 2v6.5a2 2 0 0 1-2 2H7v4.063C7 16.355 7.644 17 8.438 17H12.5v-2.5a2 2 0 0 1 2-2H21a2 2 0 0 1 2 2V21a2 2 0 0 1-2 2h-6.5a2 2 0 0 1-2-2v-2.5H8.437A2.939 2.939 0 0 1 5.5 15.562V11.5H3a2 2 0 0 1-2-2Zm2-.5a.5.5 0 0 0-.5.5v6.5a.5.5 0 0 0 .5.5h6.5a.5.5 0 0 0 .5-.5V3a.5.5 0 0 0-.5-.5ZM14.5 14a.5.5 0 0 0-.5.5V21a.5.5 0 0 0 .5.5H21a.5.5 0 0 0 .5-.5v-6.5a.5.5 0 0 0-.5-.5Z"></path></svg><span class="NavLink-module__title__Q7t0p">Actions</span><span class="NavLink-module__subtitle__X4gkW">Automate any workflow</span></div></a></li><li><a href="https://github.com/features/codespaces" data-analytics-event="{&quot;action&quot;:&quot;codespaces&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;codespaces_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-codespaces NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.5 3.75C3.5 2.784 4.284 2 5.25 2h13.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 18.75 13H5.25a1.75 1.75 0 0 1-1.75-1.75Zm-2 12c0-.966.784-1.75 1.75-1.75h17.5c.966 0 1.75.784 1.75 1.75v4a1.75 1.75 0 0 1-1.75 1.75H3.25a1.75 1.75 0 0 1-1.75-1.75ZM5.25 3.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h13.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Zm-2 12a.25.25 0 0 0-.25.25v4c0 .138.112.25.25.25h17.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25Z"></path><path d="M10 17.75a.75.75 0 0 1 .75-.75h6.5a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1-.75-.75Zm-4 0a.75.75 0 0 1 .75-.75h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1-.75-.75Z"></path></svg><span class="NavLink-module__title__Q7t0p">Codespaces</span><span class="NavLink-module__subtitle__X4gkW">Instant dev environments</span></div></a></li><li><a href="https://github.com/features/issues" data-analytics-event="{&quot;action&quot;:&quot;issues&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;issues_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-issue-opened NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M12 1c6.075 0 11 4.925 11 11s-4.925 11-11 11S1 18.075 1 12 5.925 1 12 1ZM2.5 12a9.5 9.5 0 0 0 9.5 9.5 9.5 9.5 0 0 0 9.5-9.5A9.5 9.5 0 0 0 12 2.5 9.5 9.5 0 0 0 2.5 12Zm9.5 2a2 2 0 1 1-.001-3.999A2 2 0 0 1 12 14Z"></path></svg><span class="NavLink-module__title__Q7t0p">Issues</span><span class="NavLink-module__subtitle__X4gkW">Plan and track work</span></div></a></li><li><a href="https://github.com/features/code-review" data-analytics-event="{&quot;action&quot;:&quot;code_review&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;code_review_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-code NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M15.22 4.97a.75.75 0 0 1 1.06 0l6.5 6.5a.75.75 0 0 1 0 1.06l-6.5 6.5a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L21.19 12l-5.97-5.97a.75.75 0 0 1 0-1.06Zm-6.44 0a.75.75 0 0 1 0 1.06L2.81 12l5.97 5.97a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215l-6.5-6.5a.75.75 0 0 1 0-1.06l6.5-6.5a.75.75 0 0 1 1.06 0Z"></path></svg><span class="NavLink-module__title__Q7t0p">Code Review</span><span class="NavLink-module__subtitle__X4gkW">Manage code changes</span></div></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_1m5_">APPLICATION SECURITY</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_1m5_"><li><a href="https://github.com/security/advanced-security" data-analytics-event="{&quot;action&quot;:&quot;github_advanced_security&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;github_advanced_security_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-shield-check NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M16.53 9.78a.75.75 0 0 0-1.06-1.06L11 13.19l-1.97-1.97a.75.75 0 0 0-1.06 1.06l2.5 2.5a.75.75 0 0 0 1.06 0l5-5Z"></path><path d="m12.54.637 8.25 2.675A1.75 1.75 0 0 1 22 4.976V10c0 6.19-3.771 10.704-9.401 12.83a1.704 1.704 0 0 1-1.198 0C5.77 20.705 2 16.19 2 10V4.976c0-.758.489-1.43 1.21-1.664L11.46.637a1.748 1.748 0 0 1 1.08 0Zm-.617 1.426-8.25 2.676a.249.249 0 0 0-.173.237V10c0 5.46 3.28 9.483 8.43 11.426a.199.199 0 0 0 .14 0C17.22 19.483 20.5 15.461 20.5 10V4.976a.25.25 0 0 0-.173-.237l-8.25-2.676a.253.253 0 0 0-.154 0Z"></path></svg><span class="NavLink-module__title__Q7t0p">GitHub Advanced Security</span><span class="NavLink-module__subtitle__X4gkW">Find and fix vulnerabilities</span></div></a></li><li><a href="https://github.com/security/advanced-security/code-security" data-analytics-event="{&quot;action&quot;:&quot;code_security&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;code_security_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-code-square NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M10.3 8.24a.75.75 0 0 1-.04 1.06L7.352 12l2.908 2.7a.75.75 0 1 1-1.02 1.1l-3.5-3.25a.75.75 0 0 1 0-1.1l3.5-3.25a.75.75 0 0 1 1.06.04Zm3.44 1.06a.75.75 0 1 1 1.02-1.1l3.5 3.25a.75.75 0 0 1 0 1.1l-3.5 3.25a.75.75 0 1 1-1.02-1.1l2.908-2.7-2.908-2.7Z"></path><path d="M2 3.75C2 2.784 2.784 2 3.75 2h16.5c.966 0 1.75.784 1.75 1.75v16.5A1.75 1.75 0 0 1 20.25 22H3.75A1.75 1.75 0 0 1 2 20.25Zm1.75-.25a.25.25 0 0 0-.25.25v16.5c0 .138.112.25.25.25h16.5a.25.25 0 0 0 .25-.25V3.75a.25.25 0 0 0-.25-.25Z"></path></svg><span class="NavLink-module__title__Q7t0p">Code security</span><span class="NavLink-module__subtitle__X4gkW">Secure your code as you build</span></div></a></li><li><a href="https://github.com/security/advanced-security/secret-protection" data-analytics-event="{&quot;action&quot;:&quot;secret_protection&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;secret_protection_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-lock NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6 9V7.25C6 3.845 8.503 1 12 1s6 2.845 6 6.25V9h.5a2.5 2.5 0 0 1 2.5 2.5v8a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 19.5v-8A2.5 2.5 0 0 1 5.5 9Zm-1.5 2.5v8a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1v-8a1 1 0 0 0-1-1h-13a1 1 0 0 0-1 1Zm3-4.25V9h9V7.25c0-2.67-1.922-4.75-4.5-4.75-2.578 0-4.5 2.08-4.5 4.75Z"></path></svg><span class="NavLink-module__title__Q7t0p">Secret protection</span><span class="NavLink-module__subtitle__X4gkW">Stop leaks before they start</span></div></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ NavGroup-module__hasSeparator__FnMrN"><span class="NavGroup-module__title__Wzxz2" id="_R_265_">EXPLORE</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_265_"><li><a href="https://github.com/why-github" data-analytics-event="{&quot;action&quot;:&quot;why_github&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;why_github_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Why GitHub</span></a></li><li><a href="https://docs.github.com" data-analytics-event="{&quot;action&quot;:&quot;documentation&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;documentation_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">Documentation</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li><li><a href="https://github.blog" data-analytics-event="{&quot;action&quot;:&quot;blog&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;blog_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">Blog</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li><li><a href="https://github.blog/changelog" data-analytics-event="{&quot;action&quot;:&quot;changelog&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;changelog_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">Changelog</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li><li><a href="https://github.com/marketplace" data-analytics-event="{&quot;action&quot;:&quot;marketplace&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;marketplace_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Marketplace</span></a></li></ul></div></li></ul><div class="NavDropdown-module__trailingLinkContainer__VgJGL"><a href="https://github.com/features" data-analytics-event="{&quot;action&quot;:&quot;view_all_features&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;platform&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;view_all_features_link_platform_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">View all features</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavLink-module__arrowIcon__amekg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></a></div></div></div></li><li><div class="NavDropdown-module__container__l2YeI js-details-container js-header-menu-item"><button type="button" class="NavDropdown-module__button__PEHWX js-details-target" aria-expanded="false">Solutions<svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavDropdown-module__buttonIcon__Tkl8_" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></button><div class="NavDropdown-module__dropdown__xm1jd"><ul class="NavDropdown-module__list__zuCgG"><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_m9_">BY COMPANY SIZE</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_m9_"><li><a href="https://github.com/enterprise" data-analytics-event="{&quot;action&quot;:&quot;enterprises&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;enterprises_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Enterprises</span></a></li><li><a href="https://github.com/team" data-analytics-event="{&quot;action&quot;:&quot;small_and_medium_teams&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;small_and_medium_teams_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Small and medium teams</span></a></li><li><a href="https://github.com/enterprise/startups" data-analytics-event="{&quot;action&quot;:&quot;startups&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;startups_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Startups</span></a></li><li><a href="https://github.com/solutions/industry/nonprofits" data-analytics-event="{&quot;action&quot;:&quot;nonprofits&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;nonprofits_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Nonprofits</span></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_169_">BY USE CASE</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_169_"><li><a href="https://github.com/solutions/use-case/app-modernization" data-analytics-event="{&quot;action&quot;:&quot;app_modernization&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;app_modernization_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">App Modernization</span></a></li><li><a href="https://github.com/solutions/use-case/devsecops" data-analytics-event="{&quot;action&quot;:&quot;devsecops&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;devsecops_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">DevSecOps</span></a></li><li><a href="https://github.com/solutions/use-case/devops" data-analytics-event="{&quot;action&quot;:&quot;devops&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;devops_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">DevOps</span></a></li><li><a href="https://github.com/solutions/use-case/ci-cd" data-analytics-event="{&quot;action&quot;:&quot;ci/cd&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;ci/cd_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">CI/CD</span></a></li><li><a href="https://github.com/solutions/use-case" data-analytics-event="{&quot;action&quot;:&quot;view_all_use_cases&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;view_all_use_cases_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">View all use cases</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavLink-module__arrowIcon__amekg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_1m9_">BY INDUSTRY</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_1m9_"><li><a href="https://github.com/solutions/industry/healthcare" data-analytics-event="{&quot;action&quot;:&quot;healthcare&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;healthcare_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Healthcare</span></a></li><li><a href="https://github.com/solutions/industry/financial-services" data-analytics-event="{&quot;action&quot;:&quot;financial_services&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;financial_services_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Financial services</span></a></li><li><a href="https://github.com/solutions/industry/manufacturing" data-analytics-event="{&quot;action&quot;:&quot;manufacturing&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;manufacturing_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Manufacturing</span></a></li><li><a href="https://github.com/solutions/industry/government" data-analytics-event="{&quot;action&quot;:&quot;government&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;government_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Government</span></a></li><li><a href="https://github.com/solutions/industry" data-analytics-event="{&quot;action&quot;:&quot;view_all_industries&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;view_all_industries_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">View all industries</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavLink-module__arrowIcon__amekg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></a></li></ul></div></li></ul><div class="NavDropdown-module__trailingLinkContainer__VgJGL"><a href="https://github.com/solutions" data-analytics-event="{&quot;action&quot;:&quot;view_all_solutions&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;solutions&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;view_all_solutions_link_solutions_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">View all solutions</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavLink-module__arrowIcon__amekg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></a></div></div></div></li><li><div class="NavDropdown-module__container__l2YeI js-details-container js-header-menu-item"><button type="button" class="NavDropdown-module__button__PEHWX js-details-target" aria-expanded="false">Resources<svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavDropdown-module__buttonIcon__Tkl8_" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></button><div class="NavDropdown-module__dropdown__xm1jd"><ul class="NavDropdown-module__list__zuCgG"><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_md_">EXPLORE BY TOPIC</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_md_"><li><a href="https://github.com/resources/articles?topic=ai" data-analytics-event="{&quot;action&quot;:&quot;ai&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;ai_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">AI</span></a></li><li><a href="https://github.com/resources/articles?topic=software-development" data-analytics-event="{&quot;action&quot;:&quot;software_development&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;software_development_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Software Development</span></a></li><li><a href="https://github.com/resources/articles?topic=devops" data-analytics-event="{&quot;action&quot;:&quot;devops&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;devops_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">DevOps</span></a></li><li><a href="https://github.com/resources/articles?topic=security" data-analytics-event="{&quot;action&quot;:&quot;security&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;security_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Security</span></a></li><li><a href="https://github.com/resources/articles" data-analytics-event="{&quot;action&quot;:&quot;view_all_topics&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;view_all_topics_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">View all topics</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavLink-module__arrowIcon__amekg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_16d_">EXPLORE BY TYPE</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_16d_"><li><a href="https://github.com/customer-stories" data-analytics-event="{&quot;action&quot;:&quot;customer_stories&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;customer_stories_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Customer stories</span></a></li><li><a href="https://github.com/resources/events" data-analytics-event="{&quot;action&quot;:&quot;events__webinars&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;events__webinars_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Events &amp; webinars</span></a></li><li><a href="https://github.com/resources/whitepapers" data-analytics-event="{&quot;action&quot;:&quot;ebooks__reports&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;ebooks__reports_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Ebooks &amp; reports</span></a></li><li><a href="https://github.com/solutions/executive-insights" data-analytics-event="{&quot;action&quot;:&quot;business_insights&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;business_insights_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Business insights</span></a></li><li><a href="https://skills.github.com" data-analytics-event="{&quot;action&quot;:&quot;github_skills&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;github_skills_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">GitHub Skills</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_1md_">SUPPORT &amp; SERVICES</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_1md_"><li><a href="https://docs.github.com" data-analytics-event="{&quot;action&quot;:&quot;documentation&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;documentation_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">Documentation</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li><li><a href="https://support.github.com" data-analytics-event="{&quot;action&quot;:&quot;customer_support&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;customer_support_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">Customer support</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li><li><a href="https://github.com/orgs/community/discussions" data-analytics-event="{&quot;action&quot;:&quot;community_forum&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;community_forum_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Community forum</span></a></li><li><a href="https://github.com/trust-center" data-analytics-event="{&quot;action&quot;:&quot;trust_center&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;trust_center_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Trust center</span></a></li><li><a href="https://github.com/partners" data-analytics-event="{&quot;action&quot;:&quot;partners&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;partners_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Partners</span></a></li></ul></div></li></ul><div class="NavDropdown-module__trailingLinkContainer__VgJGL"><a href="https://github.com/resources" data-analytics-event="{&quot;action&quot;:&quot;view_all_resources&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;resources&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;view_all_resources_link_resources_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">View all resources</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavLink-module__arrowIcon__amekg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></a></div></div></div></li><li><div class="NavDropdown-module__container__l2YeI js-details-container js-header-menu-item"><button type="button" class="NavDropdown-module__button__PEHWX js-details-target" aria-expanded="false">Open Source<svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavDropdown-module__buttonIcon__Tkl8_" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></button><div class="NavDropdown-module__dropdown__xm1jd"><ul class="NavDropdown-module__list__zuCgG"><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_mh_">COMMUNITY</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_mh_"><li><a href="https://github.com/open-source/sponsors" data-analytics-event="{&quot;action&quot;:&quot;github_sponsors&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;github_sponsors_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-sponsor-tiers NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M16.004 1.25C18.311 1.25 20 3.128 20 5.75c0 2.292-1.23 4.464-3.295 6.485-.481.47-.98.909-1.482 1.31l.265 1.32 1.375 7.5a.75.75 0 0 1-.982.844l-3.512-1.207a.75.75 0 0 0-.488 0L8.37 23.209a.75.75 0 0 1-.982-.844l1.378-7.512.261-1.309c-.5-.4-1-.838-1.481-1.31C5.479 10.215 4.25 8.043 4.25 5.75c0-2.622 1.689-4.5 3.996-4.5 1.55 0 2.947.752 3.832 1.967l.047.067.047-.067a4.726 4.726 0 0 1 3.612-1.962l.22-.005ZM13.89 14.531c-.418.285-.828.542-1.218.77l-.18.103a.75.75 0 0 1-.734 0l-.071-.04-.46-.272c-.282-.173-.573-.36-.868-.562l-.121.605-1.145 6.239 2.3-.79a2.248 2.248 0 0 1 1.284-.054l.18.053 2.299.79-1.141-6.226-.125-.616ZM16.004 2.75c-1.464 0-2.731.983-3.159 2.459-.209.721-1.231.721-1.44 0-.428-1.476-1.695-2.459-3.16-2.459-1.44 0-2.495 1.173-2.495 3 0 1.811 1.039 3.647 2.844 5.412a19.624 19.624 0 0 0 3.734 2.84l-.019-.011-.184-.111.147-.088a19.81 19.81 0 0 0 3.015-2.278l.37-.352C17.46 9.397 18.5 7.561 18.5 5.75c0-1.827-1.055-3-2.496-3Z"></path></svg><span class="NavLink-module__title__Q7t0p">GitHub Sponsors</span><span class="NavLink-module__subtitle__X4gkW">Fund open source developers</span></div></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_16h_">PROGRAMS</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_16h_"><li><a href="https://securitylab.github.com" data-analytics-event="{&quot;action&quot;:&quot;security_lab&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;security_lab_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">Security Lab</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li><li><a href="https://maintainers.github.com" data-analytics-event="{&quot;action&quot;:&quot;maintainer_community&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;maintainer_community_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">Maintainer Community</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li><li><a href="https://github.com/open-source/accelerator" data-analytics-event="{&quot;action&quot;:&quot;accelerator&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;accelerator_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Accelerator</span></a></li><li><a href="https://stars.github.com" data-analytics-event="{&quot;action&quot;:&quot;github_stars&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;github_stars_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">GitHub Stars</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li><li><a href="https://archiveprogram.github.com" data-analytics-event="{&quot;action&quot;:&quot;archive_program&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;archive_program_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4" target="_blank" rel="noreferrer"><span class="NavLink-module__title__Q7t0p">Archive Program</span><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-link-external NavLink-module__externalIcon__eWIry" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_1mh_">REPOSITORIES</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_1mh_"><li><a href="https://github.com/topics" data-analytics-event="{&quot;action&quot;:&quot;topics&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;topics_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Topics</span></a></li><li><a href="https://github.com/trending" data-analytics-event="{&quot;action&quot;:&quot;trending&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;trending_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Trending</span></a></li><li><a href="https://github.com/collections" data-analytics-event="{&quot;action&quot;:&quot;collections&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;open_source&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;collections_link_open_source_navbar&quot;}" class="NavLink-module__link__EG3d4"><span class="NavLink-module__title__Q7t0p">Collections</span></a></li></ul></div></li></ul></div></div></li><li><div class="NavDropdown-module__container__l2YeI js-details-container js-header-menu-item"><button type="button" class="NavDropdown-module__button__PEHWX js-details-target" aria-expanded="false">Enterprise<svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-chevron-right NavDropdown-module__buttonIcon__Tkl8_" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.22 3.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L9.94 8 6.22 4.28a.75.75 0 0 1 0-1.06Z"></path></svg></button><div class="NavDropdown-module__dropdown__xm1jd"><ul class="NavDropdown-module__list__zuCgG"><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_ml_">ENTERPRISE SOLUTIONS</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_ml_"><li><a href="https://github.com/enterprise" data-analytics-event="{&quot;action&quot;:&quot;enterprise_platform&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;enterprise&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;enterprise_platform_link_enterprise_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-stack NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M11.063 1.456a1.749 1.749 0 0 1 1.874 0l8.383 5.316a1.751 1.751 0 0 1 0 2.956l-8.383 5.316a1.749 1.749 0 0 1-1.874 0L2.68 9.728a1.751 1.751 0 0 1 0-2.956Zm1.071 1.267a.25.25 0 0 0-.268 0L3.483 8.039a.25.25 0 0 0 0 .422l8.383 5.316a.25.25 0 0 0 .268 0l8.383-5.316a.25.25 0 0 0 0-.422Z"></path><path d="M1.867 12.324a.75.75 0 0 1 1.035-.232l8.964 5.685a.25.25 0 0 0 .268 0l8.964-5.685a.75.75 0 0 1 .804 1.267l-8.965 5.685a1.749 1.749 0 0 1-1.874 0l-8.965-5.685a.75.75 0 0 1-.231-1.035Z"></path><path d="M1.867 16.324a.75.75 0 0 1 1.035-.232l8.964 5.685a.25.25 0 0 0 .268 0l8.964-5.685a.75.75 0 0 1 .804 1.267l-8.965 5.685a1.749 1.749 0 0 1-1.874 0l-8.965-5.685a.75.75 0 0 1-.231-1.035Z"></path></svg><span class="NavLink-module__title__Q7t0p">Enterprise platform</span><span class="NavLink-module__subtitle__X4gkW">AI-powered developer platform</span></div></a></li></ul></div></li><li><div class="NavGroup-module__group__W8SqJ"><span class="NavGroup-module__title__Wzxz2" id="_R_16l_">AVAILABLE ADD-ONS</span><ul class="NavGroup-module__list__UCOFy" aria-labelledby="_R_16l_"><li><a href="https://github.com/security/advanced-security" data-analytics-event="{&quot;action&quot;:&quot;github_advanced_security&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;enterprise&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;github_advanced_security_link_enterprise_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-shield-check NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M16.53 9.78a.75.75 0 0 0-1.06-1.06L11 13.19l-1.97-1.97a.75.75 0 0 0-1.06 1.06l2.5 2.5a.75.75 0 0 0 1.06 0l5-5Z"></path><path d="m12.54.637 8.25 2.675A1.75 1.75 0 0 1 22 4.976V10c0 6.19-3.771 10.704-9.401 12.83a1.704 1.704 0 0 1-1.198 0C5.77 20.705 2 16.19 2 10V4.976c0-.758.489-1.43 1.21-1.664L11.46.637a1.748 1.748 0 0 1 1.08 0Zm-.617 1.426-8.25 2.676a.249.249 0 0 0-.173.237V10c0 5.46 3.28 9.483 8.43 11.426a.199.199 0 0 0 .14 0C17.22 19.483 20.5 15.461 20.5 10V4.976a.25.25 0 0 0-.173-.237l-8.25-2.676a.253.253 0 0 0-.154 0Z"></path></svg><span class="NavLink-module__title__Q7t0p">GitHub Advanced Security</span><span class="NavLink-module__subtitle__X4gkW">Enterprise-grade security features</span></div></a></li><li><a href="https://github.com/features/copilot/copilot-business" data-analytics-event="{&quot;action&quot;:&quot;copilot_for_business&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;enterprise&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;copilot_for_business_link_enterprise_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-copilot NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M23.922 16.992c-.861 1.495-5.859 5.023-11.922 5.023-6.063 0-11.061-3.528-11.922-5.023A.641.641 0 0 1 0 16.736v-2.869a.841.841 0 0 1 .053-.22c.372-.935 1.347-2.292 2.605-2.656.167-.429.414-1.055.644-1.517a10.195 10.195 0 0 1-.052-1.086c0-1.331.282-2.499 1.132-3.368.397-.406.89-.717 1.474-.952 1.399-1.136 3.392-2.093 6.122-2.093 2.731 0 4.767.957 6.166 2.093.584.235 1.077.546 1.474.952.85.869 1.132 2.037 1.132 3.368 0 .368-.014.733-.052 1.086.23.462.477 1.088.644 1.517 1.258.364 2.233 1.721 2.605 2.656a.832.832 0 0 1 .053.22v2.869a.641.641 0 0 1-.078.256ZM12.172 11h-.344a4.323 4.323 0 0 1-.355.508C10.703 12.455 9.555 13 7.965 13c-1.725 0-2.989-.359-3.782-1.259a2.005 2.005 0 0 1-.085-.104L4 11.741v6.585c1.435.779 4.514 2.179 8 2.179 3.486 0 6.565-1.4 8-2.179v-6.585l-.098-.104s-.033.045-.085.104c-.793.9-2.057 1.259-3.782 1.259-1.59 0-2.738-.545-3.508-1.492a4.323 4.323 0 0 1-.355-.508h-.016.016Zm.641-2.935c.136 1.057.403 1.913.878 2.497.442.544 1.134.938 2.344.938 1.573 0 2.292-.337 2.657-.751.384-.435.558-1.15.558-2.361 0-1.14-.243-1.847-.705-2.319-.477-.488-1.319-.862-2.824-1.025-1.487-.161-2.192.138-2.533.529-.269.307-.437.808-.438 1.578v.021c0 .265.021.562.063.893Zm-1.626 0c.042-.331.063-.628.063-.894v-.02c-.001-.77-.169-1.271-.438-1.578-.341-.391-1.046-.69-2.533-.529-1.505.163-2.347.537-2.824 1.025-.462.472-.705 1.179-.705 2.319 0 1.211.175 1.926.558 2.361.365.414 1.084.751 2.657.751 1.21 0 1.902-.394 2.344-.938.475-.584.742-1.44.878-2.497Z"></path><path d="M14.5 14.25a1 1 0 0 1 1 1v2a1 1 0 0 1-2 0v-2a1 1 0 0 1 1-1Zm-5 0a1 1 0 0 1 1 1v2a1 1 0 0 1-2 0v-2a1 1 0 0 1 1-1Z"></path></svg><span class="NavLink-module__title__Q7t0p">Copilot for Business</span><span class="NavLink-module__subtitle__X4gkW">Enterprise-grade AI features</span></div></a></li><li><a href="https://github.com/enterprise/premium-support" data-analytics-event="{&quot;action&quot;:&quot;premium_support&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;enterprise&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;premium_support_link_enterprise_navbar&quot;}" class="NavLink-module__link__EG3d4"><div class="NavLink-module__text__XvpLQ"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-comment-discussion NavLink-module__icon__ltGNM" viewBox="0 0 24 24" width="24" height="24" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M1.75 1h12.5c.966 0 1.75.784 1.75 1.75v9.5A1.75 1.75 0 0 1 14.25 14H8.061l-2.574 2.573A1.458 1.458 0 0 1 3 15.543V14H1.75A1.75 1.75 0 0 1 0 12.25v-9.5C0 1.784.784 1 1.75 1ZM1.5 2.75v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Z"></path><path d="M22.5 8.75a.25.25 0 0 0-.25-.25h-3.5a.75.75 0 0 1 0-1.5h3.5c.966 0 1.75.784 1.75 1.75v9.5A1.75 1.75 0 0 1 22.25 20H21v1.543a1.457 1.457 0 0 1-2.487 1.03L15.939 20H10.75A1.75 1.75 0 0 1 9 18.25v-1.465a.75.75 0 0 1 1.5 0v1.465c0 .138.112.25.25.25h5.5a.75.75 0 0 1 .53.22l2.72 2.72v-2.19a.75.75 0 0 1 .75-.75h2a.25.25 0 0 0 .25-.25v-9.5Z"></path></svg><span class="NavLink-module__title__Q7t0p">Premium Support</span><span class="NavLink-module__subtitle__X4gkW">Enterprise-grade 24/7 support</span></div></a></li></ul></div></li></ul></div></div></li><li><a href="https://github.com/pricing" data-analytics-event="{&quot;action&quot;:&quot;pricing&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;context&quot;:&quot;pricing&quot;,&quot;location&quot;:&quot;navbar&quot;,&quot;label&quot;:&quot;pricing_link_pricing_navbar&quot;}" class="NavLink-module__link__EG3d4 MarketingNavigation-module__navLink__hUomM"><span class="NavLink-module__title__Q7t0p">Pricing</span></a></li></ul></nav></div>
</react-partial>


        <div class="d-flex flex-column flex-lg-row width-full flex-justify-end flex-lg-items-center text-center tmp-mt-3 tmp-mt-lg-0 text-lg-left tmp-ml-lg-3">


<qbsearch-input class="search-input" data-scope="repo:OAI/OpenAPI-Specification" data-custom-scopes-path="/search/custom_scopes" data-delete-custom-scopes-csrf="T_iVgBxUt_6N7q_4j4K7_w1a2nD4R2yaDL8NxojhFHnqs5DI4ZuD4ue5YcTLs6-L4phNFwLBdDKjYJq8oBTOhw" data-max-custom-scopes="10" data-header-redesign-enabled="false" data-initial-value="" data-blackbird-suggestions-path="/search/suggestions" data-jump-to-suggestions-path="/_graphql/GetSuggestedNavigationDestinations" data-current-repository="OAI/OpenAPI-Specification" data-current-org="OAI" data-current-owner="" data-logged-in="false" data-copilot-chat-enabled="false" data-nl-search-enabled="false" data-retain-scroll-position="true">
  <div
    class="search-input-container search-with-dialog position-relative d-flex flex-row flex-items-center tmp-mr-4 rounded"
    data-action="click:qbsearch-input#searchInputContainerClicked"
  >
      <button
        type="button"
        class="header-search-button placeholder  input-button form-control d-flex flex-1 flex-self-stretch flex-items-center no-wrap width-full py-0 pl-2 pr-0 text-left border-0 box-shadow-none"
        data-target="qbsearch-input.inputButton"
        aria-label="Search or jump to…"
        aria-haspopup="dialog"
        placeholder="Search or jump to..."
        data-hotkey=s,/
        autocapitalize="off"
        data-analytics-event="{&quot;location&quot;:&quot;navbar&quot;,&quot;action&quot;:&quot;searchbar&quot;,&quot;context&quot;:&quot;global&quot;,&quot;tag&quot;:&quot;input&quot;,&quot;label&quot;:&quot;searchbar_input_global_navbar&quot;}"
        data-action="click:qbsearch-input#handleExpand"
      >
        <div class="mr-2 color-fg-muted">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-search">
    <path d="M10.68 11.74a6 6 0 0 1-7.922-8.982 6 6 0 0 1 8.982 7.922l3.04 3.04a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215ZM11.5 7a4.499 4.499 0 1 0-8.997 0A4.499 4.499 0 0 0 11.5 7Z"></path>
</svg>
        </div>
        <span class="flex-1" data-target="qbsearch-input.inputButtonText">Search or jump to...</span>
          <div class="d-flex" data-target="qbsearch-input.hotkeyIndicator">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="20" aria-hidden="true" class="mr-1"><path fill="none" stroke="#979A9C" opacity=".4" d="M3.5.5h12c1.7 0 3 1.3 3 3v13c0 1.7-1.3 3-3 3h-12c-1.7 0-3-1.3-3-3v-13c0-1.7 1.3-3 3-3z"></path><path fill="#979A9C" d="M11.8 6L8 15.1h-.9L10.8 6h1z"></path></svg>
          </div>
      </button>

    <input type="hidden" name="type" class="js-site-search-type-field">


<div class="Overlay--hidden " data-modal-dialog-overlay>
  <modal-dialog data-action="close:qbsearch-input#handleClose cancel:qbsearch-input#handleClose" data-target="qbsearch-input.searchSuggestionsDialog" role="dialog" id="search-suggestions-dialog" aria-modal="true" aria-labelledby="search-suggestions-dialog-header" data-view-component="true" class="Overlay Overlay--width-large Overlay--height-auto">
      <h1 id="search-suggestions-dialog-header" class="sr-only">Search code, repositories, users, issues, pull requests...</h1>
    <div class="Overlay-body Overlay-body--paddingNone">

          <div data-view-component="true">        <div class="search-suggestions position-fixed width-full color-shadow-large border color-fg-default color-bg-default overflow-hidden d-flex flex-column query-builder-container"
          style="border-radius: 12px;"
          data-target="qbsearch-input.queryBuilderContainer"
          hidden
        >
          <!-- '"` --><!-- </textarea></xmp> --></option></form><form id="query-builder-test-form" action="" accept-charset="UTF-8" method="get">
  <query-builder data-target="qbsearch-input.queryBuilder" id="query-builder-query-builder-test" data-filter-key=":" data-view-component="true" class="QueryBuilder search-query-builder">
    <div class="FormControl FormControl--fullWidth">
      <label id="query-builder-test-label" for="query-builder-test" class="FormControl-label sr-only">
        Search
      </label>
      <div
        class="QueryBuilder-StyledInput width-fit "
        data-target="query-builder.styledInput"
      >
          <span id="query-builder-test-leadingvisual-wrap" class="FormControl-input-leadingVisualWrap QueryBuilder-leadingVisualWrap">
            <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-search FormControl-input-leadingVisual">
    <path d="M10.68 11.74a6 6 0 0 1-7.922-8.982 6 6 0 0 1 8.982 7.922l3.04 3.04a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215ZM11.5 7a4.499 4.499 0 1 0-8.997 0A4.499 4.499 0 0 0 11.5 7Z"></path>
</svg>
          </span>
        <div data-target="query-builder.styledInputContainer" class="QueryBuilder-StyledInputContainer">
          <div
            aria-hidden="true"
            class="QueryBuilder-StyledInputContent"
            data-target="query-builder.styledInputContent"
          ></div>
          <div class="QueryBuilder-InputWrapper">
            <div aria-hidden="true" class="QueryBuilder-Sizer" data-target="query-builder.sizer"></div>
            <input id="query-builder-test" name="query-builder-test" value="" autocomplete="off" type="text" role="combobox" spellcheck="false" aria-expanded="false" aria-describedby="validation-59aba431-2c20-4968-b75f-fc8dc2e1e47f" data-target="query-builder.input" data-action="
          input:query-builder#inputChange
          blur:query-builder#inputBlur
          keydown:query-builder#inputKeydown
          focus:query-builder#inputFocus
        " data-view-component="true" class="FormControl-input QueryBuilder-Input FormControl-medium" />
          </div>
        </div>
          <span data-target="query-builder.clearButton" hidden>
            <span class="sr-only" id="query-builder-test-clear">Clear</span>
            <button role="button" id="query-builder-test-clear-button" aria-labelledby="query-builder-test-clear query-builder-test-label" data-action="
                  click:query-builder#clear
                  focus:query-builder#clearButtonFocus
                  blur:query-builder#clearButtonBlur
                " variant="small" type="button" data-view-component="true" class="Button Button--iconOnly Button--invisible Button--medium mr-1 tmp-mr-1 px-2 tmp-px-2 py-0 tmp-py-0 d-flex flex-items-center rounded-1 color-fg-muted">  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-x-circle-fill Button-visual">
    <path d="M2.343 13.657A8 8 0 1 1 13.658 2.343 8 8 0 0 1 2.343 13.657ZM6.03 4.97a.751.751 0 0 0-1.042.018.751.751 0 0 0-.018 1.042L6.94 8 4.97 9.97a.749.749 0 0 0 .326 1.275.749.749 0 0 0 .734-.215L8 9.06l1.97 1.97a.749.749 0 0 0 1.275-.326.749.749 0 0 0-.215-.734L9.06 8l1.97-1.97a.749.749 0 0 0-.326-1.275.749.749 0 0 0-.734.215L8 6.94Z"></path>
</svg>
</button>

          </span>
      </div>
      <template id="search-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-search">
    <path d="M10.68 11.74a6 6 0 0 1-7.922-8.982 6 6 0 0 1 8.982 7.922l3.04 3.04a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215ZM11.5 7a4.499 4.499 0 1 0-8.997 0A4.499 4.499 0 0 0 11.5 7Z"></path>
</svg>
</template>

<template id="code-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-code">
    <path d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"></path>
</svg>
</template>

<template id="file-code-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-file-code">
    <path d="M4 1.75C4 .784 4.784 0 5.75 0h5.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v8.586A1.75 1.75 0 0 1 14.25 15h-9a.75.75 0 0 1 0-1.5h9a.25.25 0 0 0 .25-.25V6h-2.75A1.75 1.75 0 0 1 10 4.25V1.5H5.75a.25.25 0 0 0-.25.25v2.5a.75.75 0 0 1-1.5 0Zm1.72 4.97a.75.75 0 0 1 1.06 0l2 2a.75.75 0 0 1 0 1.06l-2 2a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734l1.47-1.47-1.47-1.47a.75.75 0 0 1 0-1.06ZM3.28 7.78 1.81 9.25l1.47 1.47a.751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018l-2-2a.75.75 0 0 1 0-1.06l2-2a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Zm8.22-6.218V4.25c0 .138.112.25.25.25h2.688l-.011-.013-2.914-2.914-.013-.011Z"></path>
</svg>
</template>

<template id="history-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-history">
    <path d="m.427 1.927 1.215 1.215a8.002 8.002 0 1 1-1.6 5.685.75.75 0 1 1 1.493-.154 6.5 6.5 0 1 0 1.18-4.458l1.358 1.358A.25.25 0 0 1 3.896 6H.25A.25.25 0 0 1 0 5.75V2.104a.25.25 0 0 1 .427-.177ZM7.75 4a.75.75 0 0 1 .75.75v2.992l2.028.812a.75.75 0 0 1-.557 1.392l-2.5-1A.751.751 0 0 1 7 8.25v-3.5A.75.75 0 0 1 7.75 4Z"></path>
</svg>
</template>

<template id="repo-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-repo">
    <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path>
</svg>
</template>

<template id="bookmark-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-bookmark">
    <path d="M3 2.75C3 1.784 3.784 1 4.75 1h6.5c.966 0 1.75.784 1.75 1.75v11.5a.75.75 0 0 1-1.227.579L8 11.722l-3.773 3.107A.751.751 0 0 1 3 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.91l3.023-2.489a.75.75 0 0 1 .954 0l3.023 2.49V2.75a.25.25 0 0 0-.25-.25Z"></path>
</svg>
</template>

<template id="plus-circle-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-plus-circle">
    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm7.25-3.25v2.5h2.5a.75.75 0 0 1 0 1.5h-2.5v2.5a.75.75 0 0 1-1.5 0v-2.5h-2.5a.75.75 0 0 1 0-1.5h2.5v-2.5a.75.75 0 0 1 1.5 0Z"></path>
</svg>
</template>

<template id="circle-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-dot-fill">
    <path d="M8 4a4 4 0 1 1 0 8 4 4 0 0 1 0-8Z"></path>
</svg>
</template>

<template id="trash-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-trash">
    <path d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"></path>
</svg>
</template>

<template id="team-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-people">
    <path d="M2 5.5a3.5 3.5 0 1 1 5.898 2.549 5.508 5.508 0 0 1 3.034 4.084.75.75 0 1 1-1.482.235 4 4 0 0 0-7.9 0 .75.75 0 0 1-1.482-.236A5.507 5.507 0 0 1 3.102 8.05 3.493 3.493 0 0 1 2 5.5ZM11 4a3.001 3.001 0 0 1 2.22 5.018 5.01 5.01 0 0 1 2.56 3.012.749.749 0 0 1-.885.954.752.752 0 0 1-.549-.514 3.507 3.507 0 0 0-2.522-2.372.75.75 0 0 1-.574-.73v-.352a.75.75 0 0 1 .416-.672A1.5 1.5 0 0 0 11 5.5.75.75 0 0 1 11 4Zm-5.5-.5a2 2 0 1 0-.001 3.999A2 2 0 0 0 5.5 3.5Z"></path>
</svg>
</template>

<template id="project-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-project">
    <path d="M1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0ZM1.5 1.75v12.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25ZM11.75 3a.75.75 0 0 1 .75.75v7.5a.75.75 0 0 1-1.5 0v-7.5a.75.75 0 0 1 .75-.75Zm-8.25.75a.75.75 0 0 1 1.5 0v5.5a.75.75 0 0 1-1.5 0ZM8 3a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 3Z"></path>
</svg>
</template>

<template id="pencil-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-pencil">
    <path d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064Zm1.238-3.763a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354Z"></path>
</svg>
</template>

<template id="copilot-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copilot">
    <path d="M7.998 15.035c-4.562 0-7.873-2.914-7.998-3.749V9.338c.085-.628.677-1.686 1.588-2.065.013-.07.024-.143.036-.218.029-.183.06-.384.126-.612-.201-.508-.254-1.084-.254-1.656 0-.87.128-1.769.693-2.484.579-.733 1.494-1.124 2.724-1.261 1.206-.134 2.262.034 2.944.765.05.053.096.108.139.165.044-.057.094-.112.143-.165.682-.731 1.738-.899 2.944-.765 1.23.137 2.145.528 2.724 1.261.566.715.693 1.614.693 2.484 0 .572-.053 1.148-.254 1.656.066.228.098.429.126.612.012.076.024.148.037.218.924.385 1.522 1.471 1.591 2.095v1.872c0 .766-3.351 3.795-8.002 3.795Zm0-1.485c2.28 0 4.584-1.11 5.002-1.433V7.862l-.023-.116c-.49.21-1.075.291-1.727.291-1.146 0-2.059-.327-2.71-.991A3.222 3.222 0 0 1 8 6.303a3.24 3.24 0 0 1-.544.743c-.65.664-1.563.991-2.71.991-.652 0-1.236-.081-1.727-.291l-.023.116v4.255c.419.323 2.722 1.433 5.002 1.433ZM6.762 2.83c-.193-.206-.637-.413-1.682-.297-1.019.113-1.479.404-1.713.7-.247.312-.369.789-.369 1.554 0 .793.129 1.171.308 1.371.162.181.519.379 1.442.379.853 0 1.339-.235 1.638-.54.315-.322.527-.827.617-1.553.117-.935-.037-1.395-.241-1.614Zm4.155-.297c-1.044-.116-1.488.091-1.681.297-.204.219-.359.679-.242 1.614.091.726.303 1.231.618 1.553.299.305.784.54 1.638.54.922 0 1.28-.198 1.442-.379.179-.2.308-.578.308-1.371 0-.765-.123-1.242-.37-1.554-.233-.296-.693-.587-1.713-.7Z"></path><path d="M6.25 9.037a.75.75 0 0 1 .75.75v1.501a.75.75 0 0 1-1.5 0V9.787a.75.75 0 0 1 .75-.75Zm4.25.75v1.501a.75.75 0 0 1-1.5 0V9.787a.75.75 0 0 1 1.5 0Z"></path>
</svg>
</template>

<template id="copilot-error-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copilot-error">
    <path d="M16 11.24c0 .112-.072.274-.21.467L13 9.688V7.862l-.023-.116c-.49.21-1.075.291-1.727.291-.198 0-.388-.009-.571-.029L6.833 5.226a4.01 4.01 0 0 0 .17-.782c.117-.935-.037-1.395-.241-1.614-.193-.206-.637-.413-1.682-.297-.683.076-1.115.231-1.395.415l-1.257-.91c.579-.564 1.413-.877 2.485-.996 1.206-.134 2.262.034 2.944.765.05.053.096.108.139.165.044-.057.094-.112.143-.165.682-.731 1.738-.899 2.944-.765 1.23.137 2.145.528 2.724 1.261.566.715.693 1.614.693 2.484 0 .572-.053 1.148-.254 1.656.066.228.098.429.126.612.012.076.024.148.037.218.924.385 1.522 1.471 1.591 2.095Zm-5.083-8.707c-1.044-.116-1.488.091-1.681.297-.204.219-.359.679-.242 1.614.091.726.303 1.231.618 1.553.299.305.784.54 1.638.54.922 0 1.28-.198 1.442-.379.179-.2.308-.578.308-1.371 0-.765-.123-1.242-.37-1.554-.233-.296-.693-.587-1.713-.7Zm2.511 11.074c-1.393.776-3.272 1.428-5.43 1.428-4.562 0-7.873-2.914-7.998-3.749V9.338c.085-.628.677-1.686 1.588-2.065.013-.07.024-.143.036-.218.029-.183.06-.384.126-.612-.18-.455-.241-.963-.252-1.475L.31 4.107A.747.747 0 0 1 0 3.509V3.49a.748.748 0 0 1 .625-.73c.156-.026.306.047.435.139l14.667 10.578a.592.592 0 0 1 .227.264.752.752 0 0 1 .046.249v.022a.75.75 0 0 1-1.19.596Zm-1.367-.991L5.635 7.964a5.128 5.128 0 0 1-.889.073c-.652 0-1.236-.081-1.727-.291l-.023.116v4.255c.419.323 2.722 1.433 5.002 1.433 1.539 0 3.089-.505 4.063-.934Z"></path>
</svg>
</template>

<template id="workflow-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-workflow">
    <path d="M0 1.75C0 .784.784 0 1.75 0h3.5C6.216 0 7 .784 7 1.75v3.5A1.75 1.75 0 0 1 5.25 7H4v4a1 1 0 0 0 1 1h4v-1.25C9 9.784 9.784 9 10.75 9h3.5c.966 0 1.75.784 1.75 1.75v3.5A1.75 1.75 0 0 1 14.25 16h-3.5A1.75 1.75 0 0 1 9 14.25v-.75H5A2.5 2.5 0 0 1 2.5 11V7h-.75A1.75 1.75 0 0 1 0 5.25Zm1.75-.25a.25.25 0 0 0-.25.25v3.5c0 .138.112.25.25.25h3.5a.25.25 0 0 0 .25-.25v-3.5a.25.25 0 0 0-.25-.25Zm9 9a.25.25 0 0 0-.25.25v3.5c0 .138.112.25.25.25h3.5a.25.25 0 0 0 .25-.25v-3.5a.25.25 0 0 0-.25-.25Z"></path>
</svg>
</template>

<template id="book-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-book">
    <path d="M0 1.75A.75.75 0 0 1 .75 1h4.253c1.227 0 2.317.59 3 1.501A3.743 3.743 0 0 1 11.006 1h4.245a.75.75 0 0 1 .75.75v10.5a.75.75 0 0 1-.75.75h-4.507a2.25 2.25 0 0 0-1.591.659l-.622.621a.75.75 0 0 1-1.06 0l-.622-.621A2.25 2.25 0 0 0 5.258 13H.75a.75.75 0 0 1-.75-.75Zm7.251 10.324.004-5.073-.002-2.253A2.25 2.25 0 0 0 5.003 2.5H1.5v9h3.757a3.75 3.75 0 0 1 1.994.574ZM8.755 4.75l-.004 7.322a3.752 3.752 0 0 1 1.992-.572H14.5v-9h-3.495a2.25 2.25 0 0 0-2.25 2.25Z"></path>
</svg>
</template>

<template id="code-review-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-code-review">
    <path d="M1.75 1h12.5c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 13H8.061l-2.574 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25v-8.5C0 1.784.784 1 1.75 1ZM1.5 2.75v8.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-8.5a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Zm5.28 1.72a.75.75 0 0 1 0 1.06L5.31 7l1.47 1.47a.751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018l-2-2a.75.75 0 0 1 0-1.06l2-2a.75.75 0 0 1 1.06 0Zm2.44 0a.75.75 0 0 1 1.06 0l2 2a.75.75 0 0 1 0 1.06l-2 2a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L10.69 7 9.22 5.53a.75.75 0 0 1 0-1.06Z"></path>
</svg>
</template>

<template id="codespaces-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-codespaces">
    <path d="M0 11.25c0-.966.784-1.75 1.75-1.75h12.5c.966 0 1.75.784 1.75 1.75v3A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25Zm2-9.5C2 .784 2.784 0 3.75 0h8.5C13.216 0 14 .784 14 1.75v5a1.75 1.75 0 0 1-1.75 1.75h-8.5A1.75 1.75 0 0 1 2 6.75Zm1.75-.25a.25.25 0 0 0-.25.25v5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-5a.25.25 0 0 0-.25-.25Zm-2 9.5a.25.25 0 0 0-.25.25v3c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-3a.25.25 0 0 0-.25-.25Z"></path><path d="M7 12.75a.75.75 0 0 1 .75-.75h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75Zm-4 0a.75.75 0 0 1 .75-.75h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1-.75-.75Z"></path>
</svg>
</template>

<template id="comment-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-comment">
    <path d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 13.25 12H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 13.543V12H2.75A1.75 1.75 0 0 1 1 10.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h4.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
</svg>
</template>

<template id="comment-discussion-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-comment-discussion">
    <path d="M1.75 1h8.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 10.25 10H7.061l-2.574 2.573A1.458 1.458 0 0 1 2 11.543V10h-.25A1.75 1.75 0 0 1 0 8.25v-5.5C0 1.784.784 1 1.75 1ZM1.5 2.75v5.5c0 .138.112.25.25.25h1a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h3.5a.25.25 0 0 0 .25-.25v-5.5a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25Zm13 2a.25.25 0 0 0-.25-.25h-.5a.75.75 0 0 1 0-1.5h.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 14.25 12H14v1.543a1.458 1.458 0 0 1-2.487 1.03L9.22 12.28a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215l2.22 2.22v-2.19a.75.75 0 0 1 .75-.75h1a.25.25 0 0 0 .25-.25Z"></path>
</svg>
</template>

<template id="organization-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-organization">
    <path d="M1.75 16A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0h8.5C11.216 0 12 .784 12 1.75v12.5c0 .085-.006.168-.018.25h2.268a.25.25 0 0 0 .25-.25V8.285a.25.25 0 0 0-.111-.208l-1.055-.703a.749.749 0 1 1 .832-1.248l1.055.703c.487.325.779.871.779 1.456v5.965A1.75 1.75 0 0 1 14.25 16h-3.5a.766.766 0 0 1-.197-.026c-.099.017-.2.026-.303.026h-3a.75.75 0 0 1-.75-.75V14h-1v1.25a.75.75 0 0 1-.75.75Zm-.25-1.75c0 .138.112.25.25.25H4v-1.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 .75.75v1.25h2.25a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25ZM3.75 6h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 3.75A.75.75 0 0 1 3.75 3h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 3.75Zm4 3A.75.75 0 0 1 7.75 6h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 7 6.75ZM7.75 3h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 9.75A.75.75 0 0 1 3.75 9h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 9.75ZM7.75 9h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"></path>
</svg>
</template>

<template id="rocket-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-rocket">
    <path d="M14.064 0h.186C15.216 0 16 .784 16 1.75v.186a8.752 8.752 0 0 1-2.564 6.186l-.458.459c-.314.314-.641.616-.979.904v3.207c0 .608-.315 1.172-.833 1.49l-2.774 1.707a.749.749 0 0 1-1.11-.418l-.954-3.102a1.214 1.214 0 0 1-.145-.125L3.754 9.816a1.218 1.218 0 0 1-.124-.145L.528 8.717a.749.749 0 0 1-.418-1.11l1.71-2.774A1.748 1.748 0 0 1 3.31 4h3.204c.288-.338.59-.665.904-.979l.459-.458A8.749 8.749 0 0 1 14.064 0ZM8.938 3.623h-.002l-.458.458c-.76.76-1.437 1.598-2.02 2.5l-1.5 2.317 2.143 2.143 2.317-1.5c.902-.583 1.74-1.26 2.499-2.02l.459-.458a7.25 7.25 0 0 0 2.123-5.127V1.75a.25.25 0 0 0-.25-.25h-.186a7.249 7.249 0 0 0-5.125 2.123ZM3.56 14.56c-.732.732-2.334 1.045-3.005 1.148a.234.234 0 0 1-.201-.064.234.234 0 0 1-.064-.201c.103-.671.416-2.273 1.15-3.003a1.502 1.502 0 1 1 2.12 2.12Zm6.94-3.935c-.088.06-.177.118-.266.175l-2.35 1.521.548 1.783 1.949-1.2a.25.25 0 0 0 .119-.213ZM3.678 8.116 5.2 5.766c.058-.09.117-.178.176-.266H3.309a.25.25 0 0 0-.213.119l-1.2 1.95ZM12 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path>
</svg>
</template>

<template id="shield-check-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-shield-check">
    <path d="m8.533.133 5.25 1.68A1.75 1.75 0 0 1 15 3.48V7c0 1.566-.32 3.182-1.303 4.682-.983 1.498-2.585 2.813-5.032 3.855a1.697 1.697 0 0 1-1.33 0c-2.447-1.042-4.049-2.357-5.032-3.855C1.32 10.182 1 8.566 1 7V3.48a1.75 1.75 0 0 1 1.217-1.667l5.25-1.68a1.748 1.748 0 0 1 1.066 0Zm-.61 1.429.001.001-5.25 1.68a.251.251 0 0 0-.174.237V7c0 1.36.275 2.666 1.057 3.859.784 1.194 2.121 2.342 4.366 3.298a.196.196 0 0 0 .154 0c2.245-.957 3.582-2.103 4.366-3.297C13.225 9.666 13.5 8.358 13.5 7V3.48a.25.25 0 0 0-.174-.238l-5.25-1.68a.25.25 0 0 0-.153 0ZM11.28 6.28l-3.5 3.5a.75.75 0 0 1-1.06 0l-1.5-1.5a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215l.97.97 2.97-2.97a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path>
</svg>
</template>

<template id="heart-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-heart">
    <path d="m8 14.25.345.666a.75.75 0 0 1-.69 0l-.008-.004-.018-.01a7.152 7.152 0 0 1-.31-.17 22.055 22.055 0 0 1-3.434-2.414C2.045 10.731 0 8.35 0 5.5 0 2.836 2.086 1 4.25 1 5.797 1 7.153 1.802 8 3.02 8.847 1.802 10.203 1 11.75 1 13.914 1 16 2.836 16 5.5c0 2.85-2.045 5.231-3.885 6.818a22.066 22.066 0 0 1-3.744 2.584l-.018.01-.006.003h-.002ZM4.25 2.5c-1.336 0-2.75 1.164-2.75 3 0 2.15 1.58 4.144 3.365 5.682A20.58 20.58 0 0 0 8 13.393a20.58 20.58 0 0 0 3.135-2.211C12.92 9.644 14.5 7.65 14.5 5.5c0-1.836-1.414-3-2.75-3-1.373 0-2.609.986-3.029 2.456a.749.749 0 0 1-1.442 0C6.859 3.486 5.623 2.5 4.25 2.5Z"></path>
</svg>
</template>

<template id="server-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-server">
    <path d="M1.75 1h12.5c.966 0 1.75.784 1.75 1.75v4c0 .372-.116.717-.314 1 .198.283.314.628.314 1v4a1.75 1.75 0 0 1-1.75 1.75H1.75A1.75 1.75 0 0 1 0 12.75v-4c0-.358.109-.707.314-1a1.739 1.739 0 0 1-.314-1v-4C0 1.784.784 1 1.75 1ZM1.5 2.75v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Zm.25 5.75a.25.25 0 0 0-.25.25v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25ZM7 4.75A.75.75 0 0 1 7.75 4h4.5a.75.75 0 0 1 0 1.5h-4.5A.75.75 0 0 1 7 4.75ZM7.75 10h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM3 4.75A.75.75 0 0 1 3.75 4h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 4.75ZM3.75 10h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"></path>
</svg>
</template>

<template id="globe-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-globe">
    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM5.78 8.75a9.64 9.64 0 0 0 1.363 4.177c.255.426.542.832.857 1.215.245-.296.551-.705.857-1.215A9.64 9.64 0 0 0 10.22 8.75Zm4.44-1.5a9.64 9.64 0 0 0-1.363-4.177c-.307-.51-.612-.919-.857-1.215a9.927 9.927 0 0 0-.857 1.215A9.64 9.64 0 0 0 5.78 7.25Zm-5.944 1.5H1.543a6.507 6.507 0 0 0 4.666 5.5c-.123-.181-.24-.365-.352-.552-.715-1.192-1.437-2.874-1.581-4.948Zm-2.733-1.5h2.733c.144-2.074.866-3.756 1.58-4.948.12-.197.237-.381.353-.552a6.507 6.507 0 0 0-4.666 5.5Zm10.181 1.5c-.144 2.074-.866 3.756-1.58 4.948-.12.197-.237.381-.353.552a6.507 6.507 0 0 0 4.666-5.5Zm2.733-1.5a6.507 6.507 0 0 0-4.666-5.5c.123.181.24.365.353.552.714 1.192 1.436 2.874 1.58 4.948Z"></path>
</svg>
</template>

<template id="issue-opened-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-issue-opened">
    <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"></path>
</svg>
</template>

<template id="device-mobile-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-device-mobile">
    <path d="M3.75 0h8.5C13.216 0 14 .784 14 1.75v12.5A1.75 1.75 0 0 1 12.25 16h-8.5A1.75 1.75 0 0 1 2 14.25V1.75C2 .784 2.784 0 3.75 0ZM3.5 1.75v12.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25ZM8 13a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path>
</svg>
</template>

<template id="package-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-package">
    <path d="m8.878.392 5.25 3.045c.54.314.872.89.872 1.514v6.098a1.75 1.75 0 0 1-.872 1.514l-5.25 3.045a1.75 1.75 0 0 1-1.756 0l-5.25-3.045A1.75 1.75 0 0 1 1 11.049V4.951c0-.624.332-1.201.872-1.514L7.122.392a1.75 1.75 0 0 1 1.756 0ZM7.875 1.69l-4.63 2.685L8 7.133l4.755-2.758-4.63-2.685a.248.248 0 0 0-.25 0ZM2.5 5.677v5.372c0 .09.047.171.125.216l4.625 2.683V8.432Zm6.25 8.271 4.625-2.683a.25.25 0 0 0 .125-.216V5.677L8.75 8.432Z"></path>
</svg>
</template>

<template id="credit-card-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-credit-card">
    <path d="M10.75 9a.75.75 0 0 0 0 1.5h1.5a.75.75 0 0 0 0-1.5h-1.5Z"></path><path d="M0 3.75C0 2.784.784 2 1.75 2h12.5c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 14H1.75A1.75 1.75 0 0 1 0 12.25ZM14.5 6.5h-13v5.75c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25Zm0-2.75a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25V5h13Z"></path>
</svg>
</template>

<template id="play-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-play">
    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path>
</svg>
</template>

<template id="gift-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-gift">
    <path d="M2 2.75A2.75 2.75 0 0 1 4.75 0c.983 0 1.873.42 2.57 1.232.268.318.497.668.68 1.042.183-.375.411-.725.68-1.044C9.376.42 10.266 0 11.25 0a2.75 2.75 0 0 1 2.45 4h.55c.966 0 1.75.784 1.75 1.75v2c0 .698-.409 1.301-1 1.582v4.918A1.75 1.75 0 0 1 13.25 16H2.75A1.75 1.75 0 0 1 1 14.25V9.332C.409 9.05 0 8.448 0 7.75v-2C0 4.784.784 4 1.75 4h.55c-.192-.375-.3-.8-.3-1.25ZM7.25 9.5H2.5v4.75c0 .138.112.25.25.25h4.5Zm1.5 0v5h4.5a.25.25 0 0 0 .25-.25V9.5Zm0-4V8h5.5a.25.25 0 0 0 .25-.25v-2a.25.25 0 0 0-.25-.25Zm-7 0a.25.25 0 0 0-.25.25v2c0 .138.112.25.25.25h5.5V5.5h-5.5Zm3-4a1.25 1.25 0 0 0 0 2.5h2.309c-.233-.818-.542-1.401-.878-1.793-.43-.502-.915-.707-1.431-.707ZM8.941 4h2.309a1.25 1.25 0 0 0 0-2.5c-.516 0-1 .205-1.43.707-.337.392-.646.975-.879 1.793Z"></path>
</svg>
</template>

<template id="code-square-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-code-square">
    <path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25Zm7.47 3.97a.75.75 0 0 1 1.06 0l2 2a.75.75 0 0 1 0 1.06l-2 2a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L10.69 8 9.22 6.53a.75.75 0 0 1 0-1.06ZM6.78 6.53 5.31 8l1.47 1.47a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215l-2-2a.75.75 0 0 1 0-1.06l2-2a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path>
</svg>
</template>

<template id="device-desktop-icon">
  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-device-desktop">
    <path d="M14.25 1c.966 0 1.75.784 1.75 1.75v7.5A1.75 1.75 0 0 1 14.25 12h-3.727c.099 1.041.52 1.872 1.292 2.757A.752.752 0 0 1 11.25 16h-6.5a.75.75 0 0 1-.565-1.243c.772-.885 1.192-1.716 1.292-2.757H1.75A1.75 1.75 0 0 1 0 10.25v-7.5C0 1.784.784 1 1.75 1ZM1.75 2.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25ZM9.018 12H6.982a5.72 5.72 0 0 1-.765 2.5h3.566a5.72 5.72 0 0 1-.765-2.5Z"></path>
</svg>
</template>

        <div class="position-relative">
                        <ul
              role="listbox"
              class="ActionListWrap QueryBuilder-ListWrap"
              aria-label="Suggestions"
              data-action="
                combobox-commit:query-builder#comboboxCommit
                mousedown:query-builder#resultsMousedown
              "
              data-target="query-builder.resultsList"
              data-persist-list=false
              id="query-builder-test-results"
              tabindex="-1"
            ></ul>

        </div>
      <div class="FormControl-inlineValidation" id="validation-59aba431-2c20-4968-b75f-fc8dc2e1e47f" hidden="hidden">
        <span class="FormControl-inlineValidation--visual">
          <svg aria-hidden="true" data-component="Octicon" height="12" viewBox="0 0 12 12" version="1.1" width="12" data-view-component="true" class="octicon octicon-alert-fill">
    <path d="M4.855.708c.5-.896 1.79-.896 2.29 0l4.675 8.351a1.312 1.312 0 0 1-1.146 1.954H1.33A1.313 1.313 0 0 1 .183 9.058ZM7 7V3H5v4Zm-1 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z"></path>
</svg>
        </span>
        <span></span>
</div>    </div>
    <div data-target="query-builder.screenReaderFeedback" aria-live="polite" aria-atomic="true" class="sr-only"></div>
</query-builder></form>
          <div class="d-flex flex-row color-fg-muted tmp-px-3 text-small color-bg-default search-feedback-prompt">
            <a target="_blank" href="https://docs.github.com/search-github/github-code-search/understanding-github-code-search-syntax" data-view-component="true" class="Link color-fg-accent text-normal ml-2 tmp-ml-2">Search syntax tips</a>            <div class="d-flex flex-1"></div>
          </div>
        </div>
</div>

    </div>
</modal-dialog></div>
  </div>
  <div data-action="click:qbsearch-input#retract" class="dark-backdrop position-fixed" hidden data-target="qbsearch-input.darkBackdrop"></div>
  <div class="color-fg-default">

<dialog-helper>
  <dialog data-target="qbsearch-input.feedbackDialog" data-action="close:qbsearch-input#handleDialogClose cancel:qbsearch-input#handleDialogClose" id="feedback-dialog" aria-modal="true" aria-labelledby="feedback-dialog-title" aria-describedby="feedback-dialog-description" data-view-component="true" class="Overlay Overlay-whenNarrow Overlay--size-medium Overlay--motion-scaleFade Overlay--disableScroll">
    <div data-view-component="true" class="Overlay-header">
  <div class="Overlay-headerContentWrap">
    <div class="Overlay-titleWrap">
      <h1 class="Overlay-title " id="feedback-dialog-title">
        Provide feedback
      </h1>

    </div>
    <div class="Overlay-actionWrap">
      <button data-close-dialog-id="feedback-dialog" aria-label="Close" aria-label="Close" type="button" data-view-component="true" class="close-button Overlay-closeButton"><svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-x">
    <path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"></path>
</svg></button>
    </div>
  </div>

</div>
      <scrollable-region data-labelled-by="feedback-dialog-title">
        <div data-view-component="true" class="Overlay-body">        <!-- '"` --><!-- </textarea></xmp> --></option></form><form id="code-search-feedback-form" data-turbo="false" action="/search/feedback" accept-charset="UTF-8" method="post"><input type="hidden" data-csrf="true" name="authenticity_token" value="hrTQuZOSy8tMLLrlCTb+M9BJwE7ZdTfIaNH5f9etjj2tqq7/XZ/7sYlgMtJqpQnJVrbYFiXVGT17R6zYpFylBg==" />
          <p>We read every piece of feedback, and take your input very seriously.</p>
          <textarea name="feedback" class="form-control width-full mb-2" style="height: 120px" id="feedback"></textarea>
          <input name="include_email" id="include_email" aria-label="Include my email address so I can be contacted" class="form-control mr-2" type="checkbox">
          <label for="include_email" style="font-weight: normal">Include my email address so I can be contacted</label>
</form></div>
      </scrollable-region>
      <div data-view-component="true" class="Overlay-footer Overlay-footer--alignEnd">          <button data-close-dialog-id="feedback-dialog" type="button" data-view-component="true" class="btn">    Cancel
</button>
          <button form="code-search-feedback-form" data-action="click:qbsearch-input#submitFeedback" type="submit" data-view-component="true" class="btn-primary btn">    Submit feedback
</button>
</div>
</dialog></dialog-helper>

    <custom-scopes data-target="qbsearch-input.customScopesManager">

<dialog-helper>
  <dialog data-target="custom-scopes.customScopesModalDialog" data-action="close:qbsearch-input#handleDialogClose cancel:qbsearch-input#handleDialogClose" id="custom-scopes-dialog" aria-modal="true" aria-labelledby="custom-scopes-dialog-title" aria-describedby="custom-scopes-dialog-description" data-view-component="true" class="Overlay Overlay-whenNarrow Overlay--size-medium Overlay--motion-scaleFade Overlay--disableScroll">
    <div data-view-component="true" class="Overlay-header Overlay-header--divided">
  <div class="Overlay-headerContentWrap">
    <div class="Overlay-titleWrap">
      <h1 class="Overlay-title " id="custom-scopes-dialog-title">
        Saved searches
      </h1>
        <h2 id="custom-scopes-dialog-description" class="Overlay-description">Use saved searches to filter your results more quickly</h2>
    </div>
    <div class="Overlay-actionWrap">
      <button data-close-dialog-id="custom-scopes-dialog" aria-label="Close" aria-label="Close" type="button" data-view-component="true" class="close-button Overlay-closeButton"><svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-x">
    <path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"></path>
</svg></button>
    </div>
  </div>

</div>
      <scrollable-region data-labelled-by="custom-scopes-dialog-title">
        <div data-view-component="true" class="Overlay-body">        <div data-target="custom-scopes.customScopesModalDialogFlash"></div>

        <div hidden class="create-custom-scope-form" data-target="custom-scopes.createCustomScopeForm">
        <!-- '"` --><!-- </textarea></xmp> --></option></form><form id="custom-scopes-dialog-form" data-turbo="false" action="/search/custom_scopes" accept-charset="UTF-8" method="post"><input type="hidden" data-csrf="true" name="authenticity_token" value="qjJ04FIEOfiiF9EZ0Yjnxim7mt5oskS1T5nkhO/8JN7Nup35GrEVSoU5HWj+CNKC1KdCNxK4iwFJjoPR4KzD9g==" />
          <div data-target="custom-scopes.customScopesModalDialogFlash"></div>

          <input type="hidden" id="custom_scope_id" name="custom_scope_id" data-target="custom-scopes.customScopesIdField">

          <div class="form-group">
            <label for="custom_scope_name">Name</label>
            <auto-check src="/search/custom_scopes/check_name" required>
              <input
                type="text"
                name="custom_scope_name"
                id="custom_scope_name"
                data-target="custom-scopes.customScopesNameField"
                class="form-control"
                autocomplete="off"
                placeholder="github-ruby"
                required
                maxlength="50">
              <input type="hidden" data-csrf="true" value="sNlqwUKC6xYpAQv/vp9xWYpgUrw0Hazw9hHjTKbh5dckHVsDIPf/4x7UTtbqGEyGX6Vt//qNKwxLntGRRsT07g==" />
            </auto-check>
          </div>

          <div class="form-group">
            <label for="custom_scope_query">Query</label>
            <input
              type="text"
              name="custom_scope_query"
              id="custom_scope_query"
              data-target="custom-scopes.customScopesQueryField"
              class="form-control"
              autocomplete="off"
              placeholder="(repo:mona/a OR repo:mona/b) AND lang:python"
              required
              maxlength="500">
          </div>

          <p class="text-small color-fg-muted">
            To see all available qualifiers, see our <a class="Link--inTextBlock" href="https://docs.github.com/search-github/github-code-search/understanding-github-code-search-syntax">documentation</a>.
          </p>
</form>        </div>

        <div data-target="custom-scopes.manageCustomScopesForm">
          <div data-target="custom-scopes.list"></div>
        </div>

</div>
      </scrollable-region>
      <div data-view-component="true" class="Overlay-footer Overlay-footer--alignEnd Overlay-footer--divided">          <button data-action="click:custom-scopes#customScopesCancel" type="button" data-view-component="true" class="btn">    Cancel
</button>
          <button form="custom-scopes-dialog-form" data-action="click:custom-scopes#customScopesSubmit" data-target="custom-scopes.customScopesSubmitButton" type="submit" data-view-component="true" class="btn-primary btn">    Create saved search
</button>
</div>
</dialog></dialog-helper>
    </custom-scopes>
  </div>
</qbsearch-input>


            <div class="position-relative HeaderMenu-link-wrap d-lg-inline-block">
              <a
                href="/login?return_to=https%3A%2F%2Fgithub.com%2FOAI%2FOpenAPI-Specification%2Fblob%2Fmain%2Fproposals%2F2024-09-01-Tags-Improvement.md"
                class="HeaderMenu-link HeaderMenu-link--sign-in HeaderMenu-button flex-shrink-0 no-underline d-none d-lg-inline-flex border border-lg-0 rounded px-2 py-1"
                style="margin-left: 12px;"
                data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;site header menu&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;SIGN_UP&quot;,&quot;originating_url&quot;:&quot;https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="580c046b2ad1df6bcec88f2fb8ee58ccf0a077fc269a350f45137aaae2ec3e9e"
                data-analytics-event="{&quot;category&quot;:&quot;Marketing nav&quot;,&quot;action&quot;:&quot;click to go to homepage&quot;,&quot;label&quot;:&quot;ref_page:Marketing;ref_cta:Sign in;ref_loc:Header&quot;}"
              >
                Sign in
              </a>
            </div>

              <a href="/signup?ref_cta=Sign+up&amp;ref_loc=header+logged+out&amp;ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E%2Fblob%2Fshow&amp;source=header-repo&amp;source_repo=OAI%2FOpenAPI-Specification"
                class="HeaderMenu-link HeaderMenu-link--sign-up HeaderMenu-button flex-shrink-0 d-flex d-lg-inline-flex no-underline border color-border-default rounded px-2 py-1"
                data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;site header menu&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;SIGN_UP&quot;,&quot;originating_url&quot;:&quot;https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="580c046b2ad1df6bcec88f2fb8ee58ccf0a077fc269a350f45137aaae2ec3e9e"
                data-analytics-event="{&quot;category&quot;:&quot;Sign up&quot;,&quot;action&quot;:&quot;click to sign up for account&quot;,&quot;label&quot;:&quot;ref_page:/&lt;user-name&gt;/&lt;repo-name&gt;/blob/show;ref_cta:Sign up;ref_loc:header logged out&quot;}"
              >
                Sign up
              </a>

                <div class="AppHeader-appearanceSettings">
    <react-partial-anchor>
      <button data-target="react-partial-anchor.anchor" id="icon-button-55faec0e-6e67-4a83-9983-f39a9d08ab5b" aria-labelledby="tooltip-e844f21a-6305-4492-a94c-b0c51baf4ec1" type="button" disabled="disabled" data-view-component="true" class="Button Button--iconOnly Button--invisible Button--medium AppHeader-button HeaderMenu-link border cursor-wait">  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-sliders Button-visual">
    <path d="M15 2.75a.75.75 0 0 1-.75.75h-4a.75.75 0 0 1 0-1.5h4a.75.75 0 0 1 .75.75Zm-8.5.75v1.25a.75.75 0 0 0 1.5 0v-4a.75.75 0 0 0-1.5 0V2H1.75a.75.75 0 0 0 0 1.5H6.5Zm1.25 5.25a.75.75 0 0 0 0-1.5h-6a.75.75 0 0 0 0 1.5h6ZM15 8a.75.75 0 0 1-.75.75H11.5V10a.75.75 0 1 1-1.5 0V6a.75.75 0 0 1 1.5 0v1.25h2.75A.75.75 0 0 1 15 8Zm-9 5.25v-2a.75.75 0 0 0-1.5 0v1.25H1.75a.75.75 0 0 0 0 1.5H4.5v1.25a.75.75 0 0 0 1.5 0v-2Zm9 0a.75.75 0 0 1-.75.75h-6a.75.75 0 0 1 0-1.5h6a.75.75 0 0 1 .75.75Z"></path>
</svg>
</button><tool-tip id="tooltip-e844f21a-6305-4492-a94c-b0c51baf4ec1" for="icon-button-55faec0e-6e67-4a83-9983-f39a9d08ab5b" popover="manual" data-direction="s" data-type="label" data-view-component="true" class="sr-only position-absolute">Appearance settings</tool-tip>

      <template data-target="react-partial-anchor.template">
        <link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/primer-react-css.244a979f6c5947c6.module.css" />
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/appearance-settings.689ddb386a317f55.module.css" />

<react-partial
  partial-name="appearance-settings"
  data-ssr="false"
  data-attempted-ssr="false"
  data-react-profiling="false"
>

  <script type="application/json" data-target="react-partial.embeddedData">{"props":{}}</script>
  <div data-target="react-partial.reactRoot"></div>
</react-partial>


      </template>
    </react-partial-anchor>
  </div>

          <button type="button" class="sr-only js-header-menu-focus-trap d-block d-lg-none">Resetting focus</button>
        </div>
      </div>
    </div>
  </div>
</header>

      <div hidden="hidden" data-view-component="true" class="js-stale-session-flash stale-session-flash flash flash-warn flash-full">

        <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-alert">
    <path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path>
</svg>
        <span class="js-stale-session-flash-signed-in" hidden>You signed in with another tab or window. <a class="Link--inTextBlock" href="">Reload</a> to refresh your session.</span>
        <span class="js-stale-session-flash-signed-out" hidden>You signed out in another tab or window. <a class="Link--inTextBlock" href="">Reload</a> to refresh your session.</span>
        <span class="js-stale-session-flash-switched" hidden>You switched accounts on another tab or window. <a class="Link--inTextBlock" href="">Reload</a> to refresh your session.</span>

    <button id="icon-button-5c9bdbf6-3e23-4687-bd23-bb75650fdb61" aria-labelledby="tooltip-2f3da4fa-d8cc-4116-ac57-9406479afa4d" type="button" data-view-component="true" class="Button Button--iconOnly Button--invisible Button--medium flash-close js-flash-close">  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-x Button-visual">
    <path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"></path>
</svg>
</button><tool-tip id="tooltip-2f3da4fa-d8cc-4116-ac57-9406479afa4d" for="icon-button-5c9bdbf6-3e23-4687-bd23-bb75650fdb61" popover="manual" data-direction="s" data-type="label" data-view-component="true" class="sr-only position-absolute">Dismiss alert</tool-tip>


</div>
    </div>

  <div id="start-of-content" class="show-on-focus"></div>


    <div id="js-flash-container" class="flash-container" data-turbo-replace>


  <template class="js-flash-template">

<div class="flash flash-full   {{ className }}">
  <div >
    <button autofocus class="flash-close js-flash-close" type="button" aria-label="Dismiss this message">
      <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-x">
    <path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"></path>
</svg>
    </button>
    <div aria-atomic="true" role="alert" class="js-flash-alert">

      <div>{{ message }}</div>

    </div>
  </div>
</div>
  </template>
</div>


  <div
    class="application-main "
    data-commit-hovercards-enabled
    data-discussion-hovercards-enabled
    data-issue-and-pr-hovercards-enabled
    data-project-hovercards-enabled
  >
        <div itemscope itemtype="http://schema.org/SoftwareSourceCode" class="">
    <main id="js-repo-pjax-container" >


    <include-fragment src="/in-product-messaging/budget-threshold-banner?organization=OAI" data-nonce="v2:e9423f9d-26fb-4cea-5439-647b0434eaa0" data-view-component="true">

  <div data-show-on-forbidden-error hidden>
    <div class="Box">
  <div class="blankslate-container">
    <div data-view-component="true" class="blankslate blankslate-spacious color-bg-default rounded-2">


      <h3 data-view-component="true" class="blankslate-heading">        Uh oh!
</h3>
      <p data-view-component="true" class="blankslate-description">        <p class="color-fg-muted my-2 mb-2 ws-normal">There was an error while loading. <a class="Link--inTextBlock" data-turbo="false" href="" aria-label="Please reload this page">Please reload this page</a>.</p>
</p>

</div>  </div>
</div>  </div>
</include-fragment>


  <div id="repository-container-header"  class="tmp-pt-3 hide-full-screen" style="background-color: var(--page-header-bgColor, var(--color-page-header-bg));" data-turbo-replace>

      <div class="d-flex flex-nowrap flex-justify-end tmp-mb-3  tmp-px-3 tmp-px-lg-5" style="gap: 1rem;">

        <div class="flex-auto min-width-0 width-fit">

  <div class=" d-flex flex-wrap flex-items-center wb-break-word f3 text-normal">
      <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-repo color-fg-muted mr-2 tmp-mr-2">
    <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"></path>
</svg>

    <span class="author flex-self-stretch" itemprop="author">
      <a class="url fn" rel="author" data-hovercard-type="organization" data-hovercard-url="/orgs/OAI/hovercard" data-octo-click="hovercard-link-click" data-octo-dimensions="link_type:self" href="/OAI">
        OAI
</a>    </span>
    <span class="mx-1 flex-self-stretch color-fg-muted">/</span>
    <strong itemprop="name" class="mr-2 flex-self-stretch">
      <a data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" href="/OAI/OpenAPI-Specification">OpenAPI-Specification</a>
    </strong>

    <span></span><span class="Label Label--secondary v-align-middle mr-1">Public</span>
  </div>


        </div>

        <div id="repository-details-container" class="flex-shrink-0" data-turbo-replace style="max-width: 70%;">
            <ul class="pagehead-actions flex-shrink-0 d-none d-md-inline" style="padding: 2px 0;">


  <li>
            <a href="/login?return_to=%2FOAI%2FOpenAPI-Specification" rel="nofollow" id="repository-details-watch-button" data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;notification subscription menu watch&quot;,&quot;repository_id&quot;:null,&quot;auth_type&quot;:&quot;LOG_IN&quot;,&quot;originating_url&quot;:&quot;https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="234ecc2af186b65bc91afa709ffd808fa9571f88857fa7156a8c34d3da4c78c0" aria-label="You must be signed in to change notification settings" data-view-component="true" class="btn-sm btn">    <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-bell mr-2 tmp-mr-2">
    <path d="M8 16a2 2 0 0 0 1.985-1.75c.017-.137-.097-.25-.235-.25h-3.5c-.138 0-.252.113-.235.25A2 2 0 0 0 8 16ZM3 5a5 5 0 0 1 10 0v2.947c0 .05.015.098.042.139l1.703 2.555A1.519 1.519 0 0 1 13.482 13H2.518a1.516 1.516 0 0 1-1.263-2.36l1.703-2.554A.255.255 0 0 0 3 7.947Zm5-3.5A3.5 3.5 0 0 0 4.5 5v2.947c0 .346-.102.683-.294.97l-1.703 2.556a.017.017 0 0 0-.003.01l.001.006c0 .002.002.004.004.006l.006.004.007.001h10.964l.007-.001.006-.004.004-.006.001-.007a.017.017 0 0 0-.003-.01l-1.703-2.554a1.745 1.745 0 0 1-.294-.97V5A3.5 3.5 0 0 0 8 1.5Z"></path>
</svg>Notifications
</a>    <tool-tip id="tooltip-6a8f2c89-0db0-4130-8aa8-a8df111bea52" for="repository-details-watch-button" popover="manual" data-direction="s" data-type="description" data-view-component="true" class="sr-only position-absolute">You must be signed in to change notification settings</tool-tip>

  </li>

  <li>
          <a icon="repo-forked" id="fork-button" href="/login?return_to=%2FOAI%2FOpenAPI-Specification" rel="nofollow" data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;repo details fork button&quot;,&quot;repository_id&quot;:17372733,&quot;auth_type&quot;:&quot;LOG_IN&quot;,&quot;originating_url&quot;:&quot;https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="1c9e88bc9014eac71e570d6a841b7a9f9f7c4b5f481804d7294cd995c6d052d4" data-view-component="true" class="btn-sm btn">    <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-repo-forked mr-2 tmp-mr-2">
    <path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"></path>
</svg>Fork
    <span id="repo-network-counter" data-pjax-replace="true" data-turbo-replace="true" title="9,161" data-view-component="true" class="Counter">9.2k</span>
</a>
  </li>

  <li>
        <div data-view-component="true" class="BtnGroup d-flex">
        <a href="/login?return_to=%2FOAI%2FOpenAPI-Specification" rel="nofollow" data-hydro-click="{&quot;event_type&quot;:&quot;authentication.click&quot;,&quot;payload&quot;:{&quot;location_in_page&quot;:&quot;star button&quot;,&quot;repository_id&quot;:17372733,&quot;auth_type&quot;:&quot;LOG_IN&quot;,&quot;originating_url&quot;:&quot;https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md&quot;,&quot;user_id&quot;:null}}" data-hydro-click-hmac="1ba2258c0ede8dbd33990b4ca8063d3c605aa34aa9ffbf66b4ace8536d33f881" aria-label="You must be signed in to star a repository" data-view-component="true" class="tooltipped tooltipped-sw btn-sm btn">    <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-star v-align-text-bottom d-inline-block mr-2 tmp-mr-2">
    <path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path>
</svg><span data-view-component="true" class="d-inline">
          Star
</span>          <span id="repo-stars-counter-star" aria-label="31094 users starred this repository" data-singular-suffix="user starred this repository" data-plural-suffix="users starred this repository" data-turbo-replace="true" title="31,094" data-view-component="true" class="Counter js-social-count">31.1k</span>
</a></div>
  </li>

</ul>

        </div>
      </div>

        <div id="responsive-meta-container" data-turbo-replace>
</div>


          <nav data-pjax="#js-repo-pjax-container" aria-label="Repository" data-view-component="true" class="js-repo-nav js-sidenav-container-pjax js-responsive-underlinenav overflow-hidden UnderlineNav px-3 tmp-px-3 px-md-4 tmp-px-md-4 px-lg-5 tmp-px-lg-5">

  <ul data-view-component="true" class="UnderlineNav-body list-style-none">
      <li data-view-component="true" class="d-inline-flex">
  <a id="code-tab" href="/OAI/OpenAPI-Specification" data-tab-item="i0code-tab" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches repo_packages repo_deployments repo_attestations /OAI/OpenAPI-Specification" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-hotkey="g c" data-command-id="repositories:go-to-code" data-react-nav="code-view" data-react-nav-anchor="code-view-repo-link" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Code&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" aria-current="page" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item selected">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-code UnderlineNav-octicon d-none d-sm-inline">
    <path d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"></path>
</svg>
        <span data-content="Code">Code</span>
          <span id="code-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="Not available" data-view-component="true" class="Counter"></span>


</a></li>
      <li data-view-component="true" class="d-inline-flex">
  <a id="issues-tab" href="/OAI/OpenAPI-Specification/issues" data-tab-item="i1issues-tab" data-selected-links="repo_issues repo_labels repo_milestones /OAI/OpenAPI-Specification/issues" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-hotkey="g i" data-command-id="repositories:go-to-issues" data-react-nav="issues-react" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Issues&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-issue-opened UnderlineNav-octicon d-none d-sm-inline">
    <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"></path>
</svg>
        <span data-content="Issues">Issues</span>
          <span id="issues-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="108" data-view-component="true" class="Counter">108</span>


</a></li>
      <li data-view-component="true" class="d-inline-flex">
  <a id="pull-requests-tab" href="/OAI/OpenAPI-Specification/pulls" data-tab-item="i2pull-requests-tab" data-selected-links="repo_pulls checks /OAI/OpenAPI-Specification/pulls" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-hotkey="g p" data-command-id="repositories:go-to-pull-requests" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Pull requests&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-git-pull-request UnderlineNav-octicon d-none d-sm-inline">
    <path d="M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z"></path>
</svg>
        <span data-content="Pull requests">Pull requests</span>
          <span id="pull-requests-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="12" data-view-component="true" class="Counter">12</span>


</a></li>
      <li data-view-component="true" class="d-inline-flex">
  <a id="discussions-tab" href="/OAI/OpenAPI-Specification/discussions" data-tab-item="i3discussions-tab" data-selected-links="repo_discussions /OAI/OpenAPI-Specification/discussions" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-hotkey="g g" data-command-id="repositories:go-to-discussions" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Discussions&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-comment-discussion UnderlineNav-octicon d-none d-sm-inline">
    <path d="M1.75 1h8.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 10.25 10H7.061l-2.574 2.573A1.458 1.458 0 0 1 2 11.543V10h-.25A1.75 1.75 0 0 1 0 8.25v-5.5C0 1.784.784 1 1.75 1ZM1.5 2.75v5.5c0 .138.112.25.25.25h1a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h3.5a.25.25 0 0 0 .25-.25v-5.5a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25Zm13 2a.25.25 0 0 0-.25-.25h-.5a.75.75 0 0 1 0-1.5h.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 14.25 12H14v1.543a1.458 1.458 0 0 1-2.487 1.03L9.22 12.28a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215l2.22 2.22v-2.19a.75.75 0 0 1 .75-.75h1a.25.25 0 0 0 .25-.25Z"></path>
</svg>
        <span data-content="Discussions">Discussions</span>
          <span id="discussions-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="Not available" data-view-component="true" class="Counter"></span>


</a></li>
      <li data-view-component="true" class="d-inline-flex">
  <a id="actions-tab" href="/OAI/OpenAPI-Specification/actions" data-tab-item="i4actions-tab" data-selected-links="repo_actions /OAI/OpenAPI-Specification/actions" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-hotkey="g a" data-command-id="repositories:go-to-actions" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Actions&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-play UnderlineNav-octicon d-none d-sm-inline">
    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path>
</svg>
        <span data-content="Actions">Actions</span>
          <span id="actions-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="Not available" data-view-component="true" class="Counter"></span>


</a></li>
      <li data-view-component="true" class="d-inline-flex">
  <a id="projects-tab" href="/OAI/OpenAPI-Specification/projects" data-tab-item="i5projects-tab" data-selected-links="repo_projects new_repo_project repo_project /OAI/OpenAPI-Specification/projects" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-hotkey="g b" data-command-id="repositories:go-to-projects" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Projects&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-table UnderlineNav-octicon d-none d-sm-inline">
    <path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25ZM6.5 6.5v8h7.75a.25.25 0 0 0 .25-.25V6.5Zm8-1.5V1.75a.25.25 0 0 0-.25-.25H6.5V5Zm-13 1.5v7.75c0 .138.112.25.25.25H5v-8ZM5 5V1.5H1.75a.25.25 0 0 0-.25.25V5Z"></path>
</svg>
        <span data-content="Projects">Projects</span>
          <span id="projects-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="Not available" data-view-component="true" class="Counter"></span>


</a></li>
      <li data-view-component="true" class="d-inline-flex">
  <a id="wiki-tab" href="/OAI/OpenAPI-Specification/wiki" data-tab-item="i6wiki-tab" data-selected-links="repo_wiki /OAI/OpenAPI-Specification/wiki" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-hotkey="g w" data-command-id="repositories:go-to-wiki" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Wiki&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-book UnderlineNav-octicon d-none d-sm-inline">
    <path d="M0 1.75A.75.75 0 0 1 .75 1h4.253c1.227 0 2.317.59 3 1.501A3.743 3.743 0 0 1 11.006 1h4.245a.75.75 0 0 1 .75.75v10.5a.75.75 0 0 1-.75.75h-4.507a2.25 2.25 0 0 0-1.591.659l-.622.621a.75.75 0 0 1-1.06 0l-.622-.621A2.25 2.25 0 0 0 5.258 13H.75a.75.75 0 0 1-.75-.75Zm7.251 10.324.004-5.073-.002-2.253A2.25 2.25 0 0 0 5.003 2.5H1.5v9h3.757a3.75 3.75 0 0 1 1.994.574ZM8.755 4.75l-.004 7.322a3.752 3.752 0 0 1 1.992-.572H14.5v-9h-3.495a2.25 2.25 0 0 0-2.25 2.25Z"></path>
</svg>
        <span data-content="Wiki">Wiki</span>
          <span id="wiki-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="Not available" data-view-component="true" class="Counter"></span>


</a></li>
      <li data-view-component="true" class="d-inline-flex">
  <a id="security-and-quality-tab" href="/OAI/OpenAPI-Specification/security" data-tab-item="i7security-and-quality-tab" data-selected-links="security overview alerts policy token_scanning code_scanning /OAI/OpenAPI-Specification/security" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-hotkey="g s" data-command-id="repositories:go-to-security" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Security and quality&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-shield UnderlineNav-octicon d-none d-sm-inline">
    <path d="M7.467.133a1.748 1.748 0 0 1 1.066 0l5.25 1.68A1.75 1.75 0 0 1 15 3.48V7c0 1.566-.32 3.182-1.303 4.682-.983 1.498-2.585 2.813-5.032 3.855a1.697 1.697 0 0 1-1.33 0c-2.447-1.042-4.049-2.357-5.032-3.855C1.32 10.182 1 8.566 1 7V3.48a1.75 1.75 0 0 1 1.217-1.667Zm.61 1.429a.25.25 0 0 0-.153 0l-5.25 1.68a.25.25 0 0 0-.174.238V7c0 1.358.275 2.666 1.057 3.86.784 1.194 2.121 2.34 4.366 3.297a.196.196 0 0 0 .154 0c2.245-.956 3.582-2.104 4.366-3.298C13.225 9.666 13.5 8.36 13.5 7V3.48a.251.251 0 0 0-.174-.237l-5.25-1.68ZM8.75 4.75v3a.75.75 0 0 1-1.5 0v-3a.75.75 0 0 1 1.5 0ZM9 10.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path>
</svg>
        <span data-content="Security and quality">Security and quality</span>
          <span id="security-and-quality-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="0" hidden="hidden" data-view-component="true" class="Counter">0</span>


</a></li>
      <li data-view-component="true" class="d-inline-flex">
  <a id="insights-tab" href="/OAI/OpenAPI-Specification/pulse" data-tab-item="i8insights-tab" data-selected-links="repo_graphs repo_contributors dependency_graph dependabot_updates pulse people community /OAI/OpenAPI-Specification/pulse" data-pjax="#repo-content-pjax-container" data-turbo-frame="repo-content-turbo-frame" data-command-id="repositories:go-to-insights" data-analytics-event="{&quot;category&quot;:&quot;Underline navbar&quot;,&quot;action&quot;:&quot;Click tab&quot;,&quot;label&quot;:&quot;Insights&quot;,&quot;target&quot;:&quot;UNDERLINE_NAV.TAB&quot;}" data-view-component="true" class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item">

              <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-graph UnderlineNav-octicon d-none d-sm-inline">
    <path d="M1.5 1.75V13.5h13.75a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0Zm14.28 2.53-5.25 5.25a.75.75 0 0 1-1.06 0L7 7.06 4.28 9.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.25-3.25a.75.75 0 0 1 1.06 0L10 7.94l4.72-4.72a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path>
</svg>
        <span data-content="Insights">Insights</span>
          <span id="insights-repo-tab-count" data-pjax-replace="" data-turbo-replace="" title="Not available" data-view-component="true" class="Counter"></span>


</a></li>
</ul>
    <div style="visibility:hidden;" data-view-component="true" class="UnderlineNav-actions js-responsive-underlinenav-overflow position-absolute pr-3 tmp-pr-3 pr-md-4 tmp-pr-md-4 pr-lg-5 tmp-pr-lg-5 right-0">      <action-menu data-select-variant="none" data-view-component="true">
  <focus-group direction="vertical" mnemonics retain>
    <button id="action-menu-61c4eeac-11e0-4feb-9335-e1ca1eee83b9-button" popovertarget="action-menu-61c4eeac-11e0-4feb-9335-e1ca1eee83b9-overlay" aria-controls="action-menu-61c4eeac-11e0-4feb-9335-e1ca1eee83b9-list" aria-haspopup="true" aria-labelledby="tooltip-1f2de1a2-5f5c-4442-a442-5fa535ea22dc" type="button" data-view-component="true" class="Button Button--iconOnly Button--secondary Button--medium UnderlineNav-item">  <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-kebab-horizontal Button-visual">
    <path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path>
</svg>
</button><tool-tip id="tooltip-1f2de1a2-5f5c-4442-a442-5fa535ea22dc" for="action-menu-61c4eeac-11e0-4feb-9335-e1ca1eee83b9-button" popover="manual" data-direction="s" data-type="label" data-view-component="true" class="sr-only position-absolute">Additional navigation options</tool-tip>


<anchored-position data-target="action-menu.overlay" id="action-menu-61c4eeac-11e0-4feb-9335-e1ca1eee83b9-overlay" anchor="action-menu-61c4eeac-11e0-4feb-9335-e1ca1eee83b9-button" align="start" side="outside-bottom" anchor-offset="normal" popover="auto" data-view-component="true">
  <div data-view-component="true" class="Overlay Overlay--size-auto">

      <div data-view-component="true" class="Overlay-body Overlay-body--paddingNone">          <action-list>
  <div data-view-component="true">
    <ul aria-labelledby="action-menu-61c4eeac-11e0-4feb-9335-e1ca1eee83b9-button" id="action-menu-61c4eeac-11e0-4feb-9335-e1ca1eee83b9-list" role="menu" data-view-component="true" class="ActionListWrap--inset ActionListWrap">
        <li hidden="hidden" data-menu-item="i0code-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-9a7a3cfa-c9f5-4ac3-b90e-5dbb4a783c7c" href="/OAI/OpenAPI-Specification" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-code">
    <path d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Code
</span>
</a>

</li>
        <li hidden="hidden" data-menu-item="i1issues-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-b0e6128c-697a-4f9d-a505-b9cb5cf75b4c" href="/OAI/OpenAPI-Specification/issues" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-issue-opened">
    <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Issues
</span>
</a>

</li>
        <li hidden="hidden" data-menu-item="i2pull-requests-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-73b9a30b-3e12-4e7e-8a98-1c43a2f5effc" href="/OAI/OpenAPI-Specification/pulls" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-git-pull-request">
    <path d="M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Pull requests
</span>
</a>

</li>
        <li hidden="hidden" data-menu-item="i3discussions-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-1d628f02-5424-430d-9a93-0da983f7edbe" href="/OAI/OpenAPI-Specification/discussions" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-comment-discussion">
    <path d="M1.75 1h8.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 10.25 10H7.061l-2.574 2.573A1.458 1.458 0 0 1 2 11.543V10h-.25A1.75 1.75 0 0 1 0 8.25v-5.5C0 1.784.784 1 1.75 1ZM1.5 2.75v5.5c0 .138.112.25.25.25h1a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h3.5a.25.25 0 0 0 .25-.25v-5.5a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25Zm13 2a.25.25 0 0 0-.25-.25h-.5a.75.75 0 0 1 0-1.5h.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 14.25 12H14v1.543a1.458 1.458 0 0 1-2.487 1.03L9.22 12.28a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215l2.22 2.22v-2.19a.75.75 0 0 1 .75-.75h1a.25.25 0 0 0 .25-.25Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Discussions
</span>
</a>

</li>
        <li hidden="hidden" data-menu-item="i4actions-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-47327735-36aa-4f94-94d0-4caf27cf2e92" href="/OAI/OpenAPI-Specification/actions" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-play">
    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Actions
</span>
</a>

</li>
        <li hidden="hidden" data-menu-item="i5projects-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-00cf2c71-4fe6-4069-a77c-f66aa4727e2b" href="/OAI/OpenAPI-Specification/projects" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-table">
    <path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25ZM6.5 6.5v8h7.75a.25.25 0 0 0 .25-.25V6.5Zm8-1.5V1.75a.25.25 0 0 0-.25-.25H6.5V5Zm-13 1.5v7.75c0 .138.112.25.25.25H5v-8ZM5 5V1.5H1.75a.25.25 0 0 0-.25.25V5Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Projects
</span>
</a>

</li>
        <li hidden="hidden" data-menu-item="i6wiki-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-15fcb219-8f19-4f15-acb7-704d05beefec" href="/OAI/OpenAPI-Specification/wiki" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-book">
    <path d="M0 1.75A.75.75 0 0 1 .75 1h4.253c1.227 0 2.317.59 3 1.501A3.743 3.743 0 0 1 11.006 1h4.245a.75.75 0 0 1 .75.75v10.5a.75.75 0 0 1-.75.75h-4.507a2.25 2.25 0 0 0-1.591.659l-.622.621a.75.75 0 0 1-1.06 0l-.622-.621A2.25 2.25 0 0 0 5.258 13H.75a.75.75 0 0 1-.75-.75Zm7.251 10.324.004-5.073-.002-2.253A2.25 2.25 0 0 0 5.003 2.5H1.5v9h3.757a3.75 3.75 0 0 1 1.994.574ZM8.755 4.75l-.004 7.322a3.752 3.752 0 0 1 1.992-.572H14.5v-9h-3.495a2.25 2.25 0 0 0-2.25 2.25Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Wiki
</span>
</a>

</li>
        <li hidden="hidden" data-menu-item="i7security-and-quality-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-01f4b0a6-2bc8-431a-883d-21c46b383ee6" href="/OAI/OpenAPI-Specification/security" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-shield">
    <path d="M7.467.133a1.748 1.748 0 0 1 1.066 0l5.25 1.68A1.75 1.75 0 0 1 15 3.48V7c0 1.566-.32 3.182-1.303 4.682-.983 1.498-2.585 2.813-5.032 3.855a1.697 1.697 0 0 1-1.33 0c-2.447-1.042-4.049-2.357-5.032-3.855C1.32 10.182 1 8.566 1 7V3.48a1.75 1.75 0 0 1 1.217-1.667Zm.61 1.429a.25.25 0 0 0-.153 0l-5.25 1.68a.25.25 0 0 0-.174.238V7c0 1.358.275 2.666 1.057 3.86.784 1.194 2.121 2.34 4.366 3.297a.196.196 0 0 0 .154 0c2.245-.956 3.582-2.104 4.366-3.298C13.225 9.666 13.5 8.36 13.5 7V3.48a.251.251 0 0 0-.174-.237l-5.25-1.68ZM8.75 4.75v3a.75.75 0 0 1-1.5 0v-3a.75.75 0 0 1 1.5 0ZM9 10.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Security and quality
</span>
</a>

</li>
        <li hidden="hidden" data-menu-item="i8insights-tab" data-targets="action-list.items" role="none" data-view-component="true" class="ActionListItem">


    <a tabindex="-1" id="item-6c67d9e6-e34e-4c7e-9c9c-73f41415a03c" href="/OAI/OpenAPI-Specification/pulse" role="menuitem" data-view-component="true" class="ActionListContent ActionListContent--visual16">
        <span class="ActionListItem-visual ActionListItem-visual--leading">
          <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-graph">
    <path d="M1.5 1.75V13.5h13.75a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0Zm14.28 2.53-5.25 5.25a.75.75 0 0 1-1.06 0L7 7.06 4.28 9.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.25-3.25a.75.75 0 0 1 1.06 0L10 7.94l4.72-4.72a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path>
</svg>
        </span>

        <span data-view-component="true" class="ActionListItem-label">
          Insights
</span>
</a>

</li>
</ul>
</div></action-list>


</div>

</div></anchored-position>  </focus-group>
</action-menu></div>
</nav>

  </div>


<turbo-frame id="repo-content-turbo-frame" target="_top" data-turbo-action="advance" class="">
    <div id="repo-content-pjax-container" class="repository-content " >


<react-app
  app-name="code-view"
  initial-path="/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md"
  style="display: block; min-height: calc(100vh - 64px);"
  data-attempted-ssr="true"
  data-ssr="true"
  data-lazy="false"
  data-alternate="false"
  data-data-router-enabled="true"
  data-react-profiling="false"
>

  <script type="application/json" data-target="react-app.embeddedData">{"payload":{"codeViewBlobRoute":{"csv":null,"csvError":null,"headerInfo":{"toc":[{"level":1,"text":"Tags Improvement","anchor":"tags-improvement","htmlText":"Tags Improvement"},{"level":2,"text":"Metadata","anchor":"metadata","htmlText":"Metadata"},{"level":2,"text":"Change Log","anchor":"change-log","htmlText":"Change Log"},{"level":2,"text":"Introduction","anchor":"introduction","htmlText":"Introduction"},{"level":2,"text":"Motivation","anchor":"motivation","htmlText":"Motivation"},{"level":3,"text":"Supporting evidence","anchor":"supporting-evidence","htmlText":"Supporting evidence"},{"level":2,"text":"Proposed solution","anchor":"proposed-solution","htmlText":"Proposed solution"},{"level":2,"text":"Detailed design","anchor":"detailed-design","htmlText":"Detailed design"},{"level":4,"text":"Tag Object","anchor":"tag-object","htmlText":"Tag Object"},{"level":5,"text":"Fixed Fields","anchor":"fixed-fields","htmlText":"Fixed Fields"},{"level":5,"text":"Tag Object Example","anchor":"tag-object-example","htmlText":"Tag Object Example"},{"level":2,"text":"Backwards compatibility","anchor":"backwards-compatibility","htmlText":"Backwards compatibility"},{"level":2,"text":"Alternatives considered","anchor":"alternatives-considered","htmlText":"Alternatives considered"}]},"issueTemplate":null,"discussionTemplate":null,"richText":"\u003carticle class=\"markdown-body entry-content container-lg\" itemprop=\"text\"\u003e\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch1 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eTags Improvement\u003c/h1\u003e\u003ca id=\"user-content-tags-improvement\" class=\"anchor\" aria-label=\"Permalink: Tags Improvement\" href=\"#tags-improvement\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch2 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eMetadata\u003c/h2\u003e\u003ca id=\"user-content-metadata\" class=\"anchor\" aria-label=\"Permalink: Metadata\" href=\"#metadata\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cmarkdown-accessiblity-table\u003e\u003ctable\u003e\n\u003cthead\u003e\n\u003ctr\u003e\n\u003cth\u003eTag\u003c/th\u003e\n\u003cth\u003eValue\u003c/th\u003e\n\u003c/tr\u003e\n\u003c/thead\u003e\n\u003ctbody\u003e\n\u003ctr\u003e\n\u003ctd\u003eProposal\u003c/td\u003e\n\u003ctd\u003e\u003ca href=\"https://github.com/OAI/OpenAPI-Specification/tree/main/proposals/%7B2024-09-01-Tags-Improvement.md%7D\"\u003e2024-09-01-Tags-Improvement\u003c/a\u003e\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003eAuthors\u003c/td\u003e\n\u003ctd\u003e\u003ca href=\"https://github.com/lornajane\"\u003eLorna Mitchell\u003c/a\u003e\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003eReview Manager\u003c/td\u003e\n\u003ctd\u003eTBD\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003eStatus\u003c/td\u003e\n\u003ctd\u003eProposal\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003eImplementations\u003c/td\u003e\n\u003ctd\u003e\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003eIssues\u003c/td\u003e\n\u003ctd\u003e\u003ca href=\"https://github.com/OAI/OpenAPI-Specification/issues/1367\" data-hovercard-type=\"issue\" data-hovercard-url=\"/OAI/OpenAPI-Specification/issues/1367/hovercard\"\u003e1367\u003c/a\u003e, \u003ca href=\"https://github.com/OAI/OpenAPI-Specification/issues/2843\" data-hovercard-type=\"issue\" data-hovercard-url=\"/OAI/OpenAPI-Specification/issues/2843/hovercard\"\u003e2843\u003c/a\u003e,\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003ePrevious Revisions\u003c/td\u003e\n\u003ctd\u003eNone, but see \u003ca href=\"https://github.com/OAI/sig-moonwalk/discussions/67\" data-hovercard-type=\"discussion\" data-hovercard-url=\"/OAI/sig-moonwalk/discussions/67/hovercard\"\u003eMoonwalk discussion\u003c/a\u003e\u003c/td\u003e\n\u003c/tr\u003e\n\u003c/tbody\u003e\n\u003c/table\u003e\u003c/markdown-accessiblity-table\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch2 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eChange Log\u003c/h2\u003e\u003ca id=\"user-content-change-log\" class=\"anchor\" aria-label=\"Permalink: Change Log\" href=\"#change-log\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cmarkdown-accessiblity-table\u003e\u003ctable\u003e\n\u003cthead\u003e\n\u003ctr\u003e\n\u003cth\u003eDate\u003c/th\u003e\n\u003cth\u003eResponsible Party\u003c/th\u003e\n\u003cth\u003eDescription\u003c/th\u003e\n\u003c/tr\u003e\n\u003c/thead\u003e\n\u003ctbody\u003e\n\u003ctr\u003e\n\u003ctd\u003e2024-09-01\u003c/td\u003e\n\u003ctd\u003e@lornajane\u003c/td\u003e\n\u003ctd\u003eInitial draft\u003c/td\u003e\n\u003c/tr\u003e\n\u003c/tbody\u003e\n\u003c/table\u003e\u003c/markdown-accessiblity-table\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch2 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eIntroduction\u003c/h2\u003e\u003ca id=\"user-content-introduction\" class=\"anchor\" aria-label=\"Permalink: Introduction\" href=\"#introduction\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cp dir=\"auto\"\u003eEvolve the existing \u003ccode\u003etags\u003c/code\u003e implementation to (optionally) support more use cases, such as giving the tags some grouping/relationships and adding more metadata.\u003c/p\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch2 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eMotivation\u003c/h2\u003e\u003ca id=\"user-content-motivation\" class=\"anchor\" aria-label=\"Permalink: Motivation\" href=\"#motivation\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cp dir=\"auto\"\u003eThe tags feature hasn't changed since the spec was still called Swagger, but it's one of the most-extended aspects of OpenAPI with most tools supporting some sort of grouping or additional metadata. One motivation for this proposal is to \"pave the cowpath\" and formalise some of the patterns from those extensions as part of the specification.\u003c/p\u003e\n\u003cp dir=\"auto\"\u003eThe existing tags implementation is also quite limiting, so users/tools feel they \"cannot\" use tags, because they are so widely implemented for documentation navigation and required exactly one tag per operation, to be used only for this single purpose or to be opted out using extensions such as \u003ccode\u003ex-traitTag\u003c/code\u003e. The result is that we see lots of extensions that add arbitrary metadata to operations, some of them even become part of the specification officially (looking at you, \u003ccode\u003edeprecated: true\u003c/code\u003e) or being so widely used that we should probably adopt them (\u003ccode\u003ex-internal\u003c/code\u003e, \u003ccode\u003ex-experimental\u003c/code\u003e). The specification does have a way of tagging operations, but it's too limited and the result is that everything has to be added as an extension field.\u003c/p\u003e\n\u003cp dir=\"auto\"\u003eOn a personal note, I work for a tool vendor and was proposing these changes internally; but the problems affect all OpenAPI users so I brought it to the main project.\u003c/p\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch3 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eSupporting evidence\u003c/h3\u003e\u003ca id=\"user-content-supporting-evidence\" class=\"anchor\" aria-label=\"Permalink: Supporting evidence\" href=\"#supporting-evidence\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cp dir=\"auto\"\u003eThere are several examples \"in the wild\" of where a better tags implementation would have helped. Here is a selection of publicly-accessible examples to illustrate some of the problems this proposal could help with:\u003c/p\u003e\n\u003cul dir=\"auto\"\u003e\n\u003cli\u003eGrouping of tags is a very common use case, almost everyone uses some sort of extra hierarchy to group the tags themselves, which makes sense as our APIs are only getting more complex, something like \u003ca href=\"https://redocly.com/docs/api-reference-docs/specification-extensions/x-tag-groups/\" rel=\"nofollow\"\u003e\u003ccode\u003ex-tagGroups\u003c/code\u003e\u003c/a\u003e is a good example - and there's a \u003ca href=\"https://github.com/OAI/OpenAPI-Specification/issues/1367\" data-hovercard-type=\"issue\" data-hovercard-url=\"/OAI/OpenAPI-Specification/issues/1367/hovercard\"\u003every active open issue on OpenAPI specification itself\u003c/a\u003e\u003c/li\u003e\n\u003cli\u003eVarious tag-alike additions exist, sometimes called \"badges\" or similar; I'd include extensions such as \u003ca href=\"https://redocly.com/docs/cli/guides/hide-apis/#step-1-add-x-internal-to-the-api-description\" rel=\"nofollow\"\u003e\u003ccode\u003ex-internal\u003c/code\u003e\u003c/a\u003e as a tag-alike since they could be tags if more than one tag (or tag type) could be applied.\u003c/li\u003e\n\u003cli\u003eAdditional display metadata is also in active use in the wild, see \u003ca href=\"https://redocly.com/docs/api-reference-docs/specification-extensions/x-display-name\" rel=\"nofollow\"\u003e\u003ccode\u003ex-displayName\u003c/code\u003e\u003c/a\u003e and this \u003ca href=\"https://github.com/OAI/OpenAPI-Specification/issues/2843\" data-hovercard-type=\"issue\" data-hovercard-url=\"/OAI/OpenAPI-Specification/issues/2843/hovercard\"\u003eOpenAPI specification issue\u003c/a\u003e\u003c/li\u003e\n\u003c/ul\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch2 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eProposed solution\u003c/h2\u003e\u003ca id=\"user-content-proposed-solution\" class=\"anchor\" aria-label=\"Permalink: Proposed solution\" href=\"#proposed-solution\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cp dir=\"auto\"\u003eOriginally proposed in a \u003ca href=\"https://github.com/OAI/sig-moonwalk/discussions/67\" data-hovercard-type=\"discussion\" data-hovercard-url=\"/OAI/sig-moonwalk/discussions/67/hovercard\"\u003eMoonwalk discussion\u003c/a\u003e, I am proposing three backwards-compatible additions to the existing tags feature:\u003c/p\u003e\n\u003cul dir=\"auto\"\u003e\n\u003cli\u003eTags get a \u003ccode\u003esummary\u003c/code\u003e alongside \u003ccode\u003ename\u003c/code\u003e and \u003ccode\u003edescription\u003c/code\u003e. In keeping with our existing practices: name is the identifier, summary is the short display content, and description is available in contexts where more information is appropriate.\u003c/li\u003e\n\u003cli\u003eA \u003ccode\u003eparent\u003c/code\u003e field is added to support a hierarchy without adding either separators or a new data type. Your tag can belong to another tag.\u003c/li\u003e\n\u003cli\u003eA \u003ccode\u003ekind\u003c/code\u003e field to explain which family of tags this tag belongs to (previously proposed as \u003ccode\u003etype\u003c/code\u003e). We'd expecting these to be \u003ccode\u003enav\u003c/code\u003e, \u003ccode\u003ebadge\u003c/code\u003e, \u003ccode\u003einternal\u003c/code\u003e and probably some other things that other tooling types would find useful.\u003c/li\u003e\n\u003c/ul\u003e\n\u003cp dir=\"auto\"\u003eAn example could look something like this:\u003c/p\u003e\n\u003cdiv class=\"highlight highlight-source-yaml notranslate position-relative overflow-auto\" dir=\"auto\" data-snippet-clipboard-copy-content=\"tags:\n- name: deprecated\n  kind: internal\n  summary: Deprecated\n  description: This operation has been deprecated and will be removed in the future. Avoid using items with this tag.\n- name: shop\n  kind: nav\n  summary: Order Online\n  description: Operations relating to the retail operations behind the [online shopping site](https://example.com/shopping).\n- name: products\n  kind: nav\n  parent: shop\n  summary: Products\n  description: View and manage the product catalog.\n- name: orders\n  kind: nav\n  parent: shop\n  summary: Online Orders\n  description: Place, fulfil and invoice orders for the online shop.\n\"\u003e\u003cpre\u003e\u003cspan class=\"pl-ent\"\u003etags\u003c/span\u003e:\n- \u003cspan class=\"pl-ent\"\u003ename\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003edeprecated\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003ekind\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003einternal\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003esummary\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eDeprecated\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003edescription\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eThis operation has been deprecated and will be removed in the future. Avoid using items with this tag.\u003c/span\u003e\n- \u003cspan class=\"pl-ent\"\u003ename\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eshop\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003ekind\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003enav\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003esummary\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eOrder Online\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003edescription\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eOperations relating to the retail operations behind the [online shopping site](https://example.com/shopping).\u003c/span\u003e\n- \u003cspan class=\"pl-ent\"\u003ename\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eproducts\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003ekind\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003enav\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003eparent\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eshop\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003esummary\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eProducts\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003edescription\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eView and manage the product catalog.\u003c/span\u003e\n- \u003cspan class=\"pl-ent\"\u003ename\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eorders\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003ekind\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003enav\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003eparent\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eshop\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003esummary\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eOnline Orders\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003edescription\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003ePlace, fulfil and invoice orders for the online shop.\u003c/span\u003e\n\u003c/pre\u003e\u003c/div\u003e\n\u003cp dir=\"auto\"\u003eRather than making an allowed list of kinds, we will instead leave that open for user extension and keep a list of the recommended/expected types in a registry and evolve that as conventions emerge.\u003c/p\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch2 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eDetailed design\u003c/h2\u003e\u003ca id=\"user-content-detailed-design\" class=\"anchor\" aria-label=\"Permalink: Detailed design\" href=\"#detailed-design\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cp dir=\"auto\"\u003eThe following section is an updated specification section, for the top-level tags object only (no other changes are needed):\u003c/p\u003e\n\u003chr\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch4 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eTag Object\u003c/h4\u003e\u003ca id=\"user-content-tag-object\" class=\"anchor\" aria-label=\"Permalink: Tag Object\" href=\"#tag-object\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cp dir=\"auto\"\u003eAdds metadata to a single tag that is used by the \u003ca href=\"#operation-object\"\u003eOperation Object\u003c/a\u003e.\nEach tag used in the Operation Object instances MAY have a Tag Object defined.\u003c/p\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch5 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eFixed Fields\u003c/h5\u003e\u003ca id=\"user-content-fixed-fields\" class=\"anchor\" aria-label=\"Permalink: Fixed Fields\" href=\"#fixed-fields\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cmarkdown-accessiblity-table\u003e\u003ctable\u003e\n\u003cthead\u003e\n\u003ctr\u003e\n\u003cth\u003eField Name\u003c/th\u003e\n\u003cth align=\"center\"\u003eType\u003c/th\u003e\n\u003cth\u003eDescription\u003c/th\u003e\n\u003c/tr\u003e\n\u003c/thead\u003e\n\u003ctbody\u003e\n\u003ctr\u003e\n\u003ctd\u003e\u003ca name=\"user-content-tagname\"\u003e\u003c/a\u003ename\u003c/td\u003e\n\u003ctd align=\"center\"\u003e\u003ccode\u003estring\u003c/code\u003e\u003c/td\u003e\n\u003ctd\u003e\u003cstrong\u003eREQUIRED\u003c/strong\u003e. The name of the tag. Use this value in the \u003ccode\u003etags\u003c/code\u003e array of an Operation.\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003e\u003ca name=\"user-content-tagsummary\"\u003e\u003c/a\u003esummary\u003c/td\u003e\n\u003ctd align=\"center\"\u003e\u003ccode\u003estring\u003c/code\u003e\u003c/td\u003e\n\u003ctd\u003eA short summary of the tag, used for display purposes.\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003e\u003ca name=\"user-content-tagdescription\"\u003e\u003c/a\u003edescription\u003c/td\u003e\n\u003ctd align=\"center\"\u003e\u003ccode\u003estring\u003c/code\u003e\u003c/td\u003e\n\u003ctd\u003eA description for the tag. \u003ca href=\"https://spec.commonmark.org/\" rel=\"nofollow\"\u003eCommonMark syntax\u003c/a\u003e MAY be used for rich text representation.\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003e\u003ca name=\"user-content-tagexternaldocs\"\u003e\u003c/a\u003eexternalDocs\u003c/td\u003e\n\u003ctd align=\"center\"\u003e\u003ca href=\"#external-documentation-object\"\u003eExternal Documentation Object\u003c/a\u003e\u003c/td\u003e\n\u003ctd\u003eAdditional external documentation for this tag.\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003e\u003ca name=\"user-content-tagparent\"\u003e\u003c/a\u003eparent\u003c/td\u003e\n\u003ctd align=\"center\"\u003e\u003ccode\u003estring\u003c/code\u003e\u003c/td\u003e\n\u003ctd\u003eThe \u003ccode\u003ename\u003c/code\u003e of a tag that this tags is nested under. The named tag MUST exist in the API description, and circular references between parent and child tags MUST NOT be used.\u003c/td\u003e\n\u003c/tr\u003e\n\u003ctr\u003e\n\u003ctd\u003e\u003ca name=\"user-content-tagkind\"\u003e\u003c/a\u003ekind\u003c/td\u003e\n\u003ctd align=\"center\"\u003e\u003ccode\u003estring\u003c/code\u003e\u003c/td\u003e\n\u003ctd\u003eA machine-readable string to categorize what sort of tag it is. Common uses are \u003ccode\u003enav\u003c/code\u003e for Navigation, \u003ccode\u003ebadge\u003c/code\u003e for badges, \u003ccode\u003einternal\u003c/code\u003e for internal APIs, but any string value can be used. A registry of known values is available.\u003c/td\u003e\n\u003c/tr\u003e\n\u003c/tbody\u003e\n\u003c/table\u003e\u003c/markdown-accessiblity-table\u003e\n\u003cp dir=\"auto\"\u003eThis object MAY be extended with \u003ca href=\"#specification-extensions\"\u003eSpecification Extensions\u003c/a\u003e.\u003c/p\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch5 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eTag Object Example\u003c/h5\u003e\u003ca id=\"user-content-tag-object-example\" class=\"anchor\" aria-label=\"Permalink: Tag Object Example\" href=\"#tag-object-example\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cdiv class=\"highlight highlight-source-json notranslate position-relative overflow-auto\" dir=\"auto\" data-snippet-clipboard-copy-content=\"{\n  \u0026quot;name\u0026quot;: \u0026quot;account-updates\u0026quot;,\n  \u0026quot;summary\u0026quot;: \u0026quot;Account Updates\u0026quot;,\n  \u0026quot;description\u0026quot;: \u0026quot;Account update operations\u0026quot;,\n  \u0026quot;kind\u0026quot;: \u0026quot;nav\u0026quot;\n},\n{\n  \u0026quot;name\u0026quot;: \u0026quot;partner\u0026quot;,\n  \u0026quot;summary\u0026quot;: \u0026quot;Partner\u0026quot;,\n  \u0026quot;description\u0026quot;: \u0026quot;Operations available to the partners network\u0026quot;,\n  \u0026quot;parent\u0026quot;: \u0026quot;external\u0026quot;,\n  \u0026quot;kind\u0026quot;: \u0026quot;audience\u0026quot;\n},\n{\n  \u0026quot;name\u0026quot;: \u0026quot;external\u0026quot;,\n  \u0026quot;summary\u0026quot;: \u0026quot;External\u0026quot;,\n  \u0026quot;description\u0026quot;: \u0026quot;Operations available to external consumers\u0026quot;,\n  \u0026quot;kind\u0026quot;: \u0026quot;audience\u0026quot;\n}\"\u003e\u003cpre\u003e{\n  \u003cspan class=\"pl-ent\"\u003e\"name\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eaccount-updates\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"summary\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eAccount Updates\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"description\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eAccount update operations\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"kind\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003enav\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e\n},\n{\n  \u003cspan class=\"pl-ent\"\u003e\"name\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003epartner\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"summary\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003ePartner\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"description\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eOperations available to the partners network\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"parent\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eexternal\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"kind\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eaudience\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e\n},\n{\n  \u003cspan class=\"pl-ent\"\u003e\"name\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eexternal\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"summary\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eExternal\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"description\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eOperations available to external consumers\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e,\n  \u003cspan class=\"pl-ent\"\u003e\"kind\"\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003e\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003eaudience\u003cspan class=\"pl-pds\"\u003e\"\u003c/span\u003e\u003c/span\u003e\n}\u003c/pre\u003e\u003c/div\u003e\n\u003cdiv class=\"highlight highlight-source-yaml notranslate position-relative overflow-auto\" dir=\"auto\" data-snippet-clipboard-copy-content=\"- name: account-updates\n  summary: Account Updates\n  description: Account update operations\n  kind: nav\n\n- name: partner\n  summary: Partner\n  description: Operations available to the partners network\n  parent: external\n  kind: audience\n\n- name: external\n  summary: External\n  description: Operations available to external consumers\n  kind: audience\"\u003e\u003cpre\u003e- \u003cspan class=\"pl-ent\"\u003ename\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eaccount-updates\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003esummary\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eAccount Updates\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003edescription\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eAccount update operations\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003ekind\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003enav\u003c/span\u003e\n\n- \u003cspan class=\"pl-ent\"\u003ename\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003epartner\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003esummary\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003ePartner\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003edescription\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eOperations available to the partners network\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003eparent\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eexternal\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003ekind\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eaudience\u003c/span\u003e\n\n- \u003cspan class=\"pl-ent\"\u003ename\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eexternal\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003esummary\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eExternal\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003edescription\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eOperations available to external consumers\u003c/span\u003e\n  \u003cspan class=\"pl-ent\"\u003ekind\u003c/span\u003e: \u003cspan class=\"pl-s\"\u003eaudience\u003c/span\u003e\u003c/pre\u003e\u003c/div\u003e\n\u003chr\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch2 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eBackwards compatibility\u003c/h2\u003e\u003ca id=\"user-content-backwards-compatibility\" class=\"anchor\" aria-label=\"Permalink: Backwards compatibility\" href=\"#backwards-compatibility\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cp dir=\"auto\"\u003eAll new fields are optional, so existing API descriptions will remain valid and useful.\nSome users may wish to adopt some of the following steps on upgrade:\u003c/p\u003e\n\u003cul dir=\"auto\"\u003e\n\u003cli\u003eSet \u003ccode\u003ekind: nav\u003c/code\u003e if their existing tags are currently used for navigation entries in documentation tooling.\u003c/li\u003e\n\u003cli\u003eChange \u003ccode\u003ex-displayName\u003c/code\u003e in \u003ccode\u003etag\u003c/code\u003e objects to \u003ccode\u003esummary\u003c/code\u003e instead.\u003c/li\u003e\n\u003cli\u003eAdd a tag to replace each \u003ccode\u003ex-tagGroups\u003c/code\u003e entry, and set the \u003ccode\u003eparent\u003c/code\u003e field for each of the tags in the groups.\u003c/li\u003e\n\u003cli\u003eChange \u003ccode\u003ex-badges\u003c/code\u003e extensions to instead be a tag with \u003ccode\u003ekind: badge\u003c/code\u003e.\u003c/li\u003e\n\u003cli\u003eChange features like \u003ccode\u003ex-internal\u003c/code\u003e to be a tag with a specific \u003ccode\u003ekind\u003c/code\u003e set. Similarly some lifecycle use cases such as \u003ccode\u003ex-beta\u003c/code\u003e could be replaced with tags.\u003c/li\u003e\n\u003c/ul\u003e\n\u003cdiv class=\"markdown-heading\" dir=\"auto\"\u003e\u003ch2 tabindex=\"-1\" class=\"heading-element\" dir=\"auto\"\u003eAlternatives considered\u003c/h2\u003e\u003ca id=\"user-content-alternatives-considered\" class=\"anchor\" aria-label=\"Permalink: Alternatives considered\" href=\"#alternatives-considered\"\u003e\u003csvg data-component=\"Octicon\" class=\"octicon octicon-link\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" height=\"16\" aria-hidden=\"true\"\u003e\u003cpath d=\"m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z\"\u003e\u003c/path\u003e\u003c/svg\u003e\u003c/a\u003e\u003c/div\u003e\n\u003cul dir=\"auto\"\u003e\n\u003cli\u003e\n\u003cp dir=\"auto\"\u003eContinue to use tags as-is, and extend the spec for each use case that users need rather than providing an open metadata implementation.\nWe've been slow to iterate and I would rather \"open\" the options than try to control them.\nThe API space evolves quite quickly.\u003c/p\u003e\n\u003c/li\u003e\n\u003cli\u003e\n\u003cp dir=\"auto\"\u003eSet \u003ccode\u003echildren\u003c/code\u003e rather than \u003ccode\u003eparent\u003c/code\u003e on the tags and operate a top-down relationship.\nThe suggestion of allowing multiple links or a graph approach was also mentioned.\nIn both cases, there are good ideas in every direction, but our responsibility is to implement a structure that users can easily understand and maintain.\u003c/p\u003e\n\u003c/li\u003e\n\u003c/ul\u003e\n\u003c/article\u003e","richTextTruncated":false,"renderedFileInfo":null,"symbols":{"timed_out":false,"not_analyzed":false,"symbols":[{"name":"Tags Improvement","kind":"section_1","ident_start":2,"ident_end":18,"extent_start":0,"extent_end":8830,"fully_qualified_name":"Tags Improvement","ident_utf16":{"start":{"line_number":0,"utf16_col":2},"end":{"line_number":0,"utf16_col":18}},"extent_utf16":{"start":{"line_number":0,"utf16_col":0},"end":{"line_number":165,"utf16_col":0}}},{"name":"Metadata","kind":"section_2","ident_start":24,"ident_end":32,"extent_start":21,"extent_end":592,"fully_qualified_name":"Metadata","ident_utf16":{"start":{"line_number":3,"utf16_col":3},"end":{"line_number":3,"utf16_col":11}},"extent_utf16":{"start":{"line_number":3,"utf16_col":0},"end":{"line_number":15,"utf16_col":0}}},{"name":"Change Log","kind":"section_2","ident_start":595,"ident_end":605,"extent_start":592,"extent_end":732,"fully_qualified_name":"Change Log","ident_utf16":{"start":{"line_number":15,"utf16_col":3},"end":{"line_number":15,"utf16_col":13}},"extent_utf16":{"start":{"line_number":15,"utf16_col":0},"end":{"line_number":21,"utf16_col":0}}},{"name":"Introduction","kind":"section_2","ident_start":735,"ident_end":747,"extent_start":732,"extent_end":910,"fully_qualified_name":"Introduction","ident_utf16":{"start":{"line_number":21,"utf16_col":3},"end":{"line_number":21,"utf16_col":15}},"extent_utf16":{"start":{"line_number":21,"utf16_col":0},"end":{"line_number":25,"utf16_col":0}}},{"name":"Motivation","kind":"section_2","ident_start":913,"ident_end":923,"extent_start":910,"extent_end":3452,"fully_qualified_name":"Motivation","ident_utf16":{"start":{"line_number":25,"utf16_col":3},"end":{"line_number":25,"utf16_col":13}},"extent_utf16":{"start":{"line_number":25,"utf16_col":0},"end":{"line_number":41,"utf16_col":0}}},{"name":"Supporting evidence","kind":"section_3","ident_start":2186,"ident_end":2205,"extent_start":2182,"extent_end":3452,"fully_qualified_name":"Supporting evidence","ident_utf16":{"start":{"line_number":33,"utf16_col":4},"end":{"line_number":33,"utf16_col":23}},"extent_utf16":{"start":{"line_number":33,"utf16_col":0},"end":{"line_number":41,"utf16_col":0}}},{"name":"Proposed solution","kind":"section_2","ident_start":3455,"ident_end":3472,"extent_start":3452,"extent_end":5136,"fully_qualified_name":"Proposed solution","ident_utf16":{"start":{"line_number":41,"utf16_col":3},"end":{"line_number":41,"utf16_col":20}},"extent_utf16":{"start":{"line_number":41,"utf16_col":0},"end":{"line_number":76,"utf16_col":0}}},{"name":"Detailed design","kind":"section_2","ident_start":5139,"ident_end":5154,"extent_start":5136,"extent_end":7502,"fully_qualified_name":"Detailed design","ident_utf16":{"start":{"line_number":76,"utf16_col":3},"end":{"line_number":76,"utf16_col":18}},"extent_utf16":{"start":{"line_number":76,"utf16_col":0},"end":{"line_number":144,"utf16_col":0}}},{"name":"Tag Object","kind":"section_4","ident_start":5292,"ident_end":5302,"extent_start":5287,"extent_end":7502,"fully_qualified_name":"Tag Object","ident_utf16":{"start":{"line_number":82,"utf16_col":5},"end":{"line_number":82,"utf16_col":15}},"extent_utf16":{"start":{"line_number":82,"utf16_col":0},"end":{"line_number":144,"utf16_col":0}}},{"name":"Fixed Fields","kind":"section_5","ident_start":5479,"ident_end":5491,"extent_start":5473,"extent_end":6673,"fully_qualified_name":"Fixed Fields","ident_utf16":{"start":{"line_number":87,"utf16_col":6},"end":{"line_number":87,"utf16_col":18}},"extent_utf16":{"start":{"line_number":87,"utf16_col":0},"end":{"line_number":100,"utf16_col":0}}},{"name":"Tag Object Example","kind":"section_5","ident_start":6679,"ident_end":6697,"extent_start":6673,"extent_end":7502,"fully_qualified_name":"Tag Object Example","ident_utf16":{"start":{"line_number":100,"utf16_col":6},"end":{"line_number":100,"utf16_col":24}},"extent_utf16":{"start":{"line_number":100,"utf16_col":0},"end":{"line_number":144,"utf16_col":0}}},{"name":"Backwards compatibility","kind":"section_2","ident_start":7505,"ident_end":7528,"extent_start":7502,"extent_end":8202,"fully_qualified_name":"Backwards compatibility","ident_utf16":{"start":{"line_number":144,"utf16_col":3},"end":{"line_number":144,"utf16_col":26}},"extent_utf16":{"start":{"line_number":144,"utf16_col":0},"end":{"line_number":155,"utf16_col":0}}},{"name":"Alternatives considered","kind":"section_2","ident_start":8205,"ident_end":8228,"extent_start":8202,"extent_end":8830,"fully_qualified_name":"Alternatives considered","ident_utf16":{"start":{"line_number":155,"utf16_col":3},"end":{"line_number":155,"utf16_col":26}},"extent_utf16":{"start":{"line_number":155,"utf16_col":0},"end":{"line_number":165,"utf16_col":0}}}]}},"codeViewLayoutRoute":{"repo":{"id":17372733,"defaultBranch":"main","name":"OpenAPI-Specification","ownerLogin":"OAI","currentUserCanPush":false,"isFork":false,"isEmpty":false,"createdAt":"2014-03-03T16:53:36.000Z","ownerAvatar":"https://avatars.githubusercontent.com/u/16343502?v=4","public":true,"private":false,"isOrgOwned":true},"currentUser":null,"uploadToken":"gWPp60CYOgCAc3nYd_dA5yJ6Yk24qfQ2JJH3CVCStTg_HakFvXw2aFtMHjlg04pj8y5O6L22PaFxZfZ_GW30Yg","allShortcutsEnabled":false,"treeExpanded":true,"path":"proposals/2024-09-01-Tags-Improvement.md","symbolsExpanded":false,"refInfo":{"name":"main","listCacheKey":"v0:1784274187.0","canEdit":false,"currentOid":"8e166da300c64bb7144938fec518b8e3f4cae715"},"helpUrl":"https://docs.github.com","findFileWorkerPath":"/assets-cdn/worker/find-file-worker-e47c88e0e1d9a6e9.js","findInFileWorkerPath":"/assets-cdn/worker/find-in-file-worker-46708daff7a1f480.js","githubDevUrl":null},"codeViewFileTreeLayoutRoute":{"fileTree":{"proposals":{"items":[{"name":"Alternative-Schema","path":"proposals/Alternative-Schema","contentType":"directory"},{"name":"Overlays","path":"proposals/Overlays","contentType":"directory"},{"name":"2019-01-01-Proposal-Template.md","path":"proposals/2019-01-01-Proposal-Template.md","contentType":"file"},{"name":"2019-03-15-Alternative-Schema.md","path":"proposals/2019-03-15-Alternative-Schema.md","contentType":"file"},{"name":"2019-07-17-Webhooks.md","path":"proposals/2019-07-17-Webhooks.md","contentType":"file"},{"name":"2019-10-31-Clarify-Nullable.md","path":"proposals/2019-10-31-Clarify-Nullable.md","contentType":"file"},{"name":"2019-12-24-Overlays.md","path":"proposals/2019-12-24-Overlays.md","contentType":"file"},{"name":"2020-10-28-Experimental.md","path":"proposals/2020-10-28-Experimental.md","contentType":"file"},{"name":"2024-08-01-Self-Identification.md","path":"proposals/2024-08-01-Self-Identification.md","contentType":"file"},{"name":"2024-09-01-Tags-Improvement.md","path":"proposals/2024-09-01-Tags-Improvement.md","contentType":"file"},{"name":"2025-03-20-URIs-for-Tags.md","path":"proposals/2025-03-20-URIs-for-Tags.md","contentType":"file"}],"totalCount":11},"":{"items":[{"name":".github","path":".github","contentType":"directory"},{"name":"_archive_","path":"_archive_","contentType":"directory"},{"name":"proposals","path":"proposals","contentType":"directory"},{"name":"scripts","path":"scripts","contentType":"directory"},{"name":"tests","path":"tests","contentType":"directory"},{"name":"versions","path":"versions","contentType":"directory"},{"name":".gitattributes","path":".gitattributes","contentType":"file"},{"name":".gitignore","path":".gitignore","contentType":"file"},{"name":".gitmodules","path":".gitmodules","contentType":"file"},{"name":".linkspector.yml","path":".linkspector.yml","contentType":"file"},{"name":".markdownlint.yaml","path":".markdownlint.yaml","contentType":"file"},{"name":"AI.md","path":"AI.md","contentType":"file"},{"name":"CONTRIBUTING.md","path":"CONTRIBUTING.md","contentType":"file"},{"name":"EDITORS.md","path":"EDITORS.md","contentType":"file"},{"name":"GOVERNANCE.md","path":"GOVERNANCE.md","contentType":"file"},{"name":"IMPLEMENTATIONS.md","path":"IMPLEMENTATIONS.md","contentType":"file"},{"name":"LICENSE","path":"LICENSE","contentType":"file"},{"name":"MAINTAINERS.md","path":"MAINTAINERS.md","contentType":"file"},{"name":"README.md","path":"README.md","contentType":"file"},{"name":"SECURITY_CONSIDERATIONS.md","path":"SECURITY_CONSIDERATIONS.md","contentType":"file"},{"name":"SPECIAL_INTEREST_GROUPS.md","path":"SPECIAL_INTEREST_GROUPS.md","contentType":"file"},{"name":"TOB.md","path":"TOB.md","contentType":"file"},{"name":"package-lock.json","path":"package-lock.json","contentType":"file"},{"name":"package.json","path":"package.json","contentType":"file"},{"name":"spec.markdownlint.yaml","path":"spec.markdownlint.yaml","contentType":"file"},{"name":"style-guide.md","path":"style-guide.md","contentType":"file"},{"name":"vitest.config.mjs","path":"vitest.config.mjs","contentType":"file"}],"totalCount":27}},"fileTreeProcessingTime":20.958968000000002,"foldersToFetch":[]},"codeViewBlobLayoutRoute":{"codeLineWrapEnabled":false,"refInfo":{"name":"main","listCacheKey":"v0:1784274187.0","canEdit":false,"refType":"branch","currentOid":"8e166da300c64bb7144938fec518b8e3f4cae715","canEditOnDefaultBranch":false,"fileExistsOnDefault":true},"path":"proposals/2024-09-01-Tags-Improvement.md","blob":{"copilotSWEAgentEnabled":false,"dependabotInfo":{"showConfigurationBanner":false,"configFilePath":null,"networkDependabotPath":"/OAI/OpenAPI-Specification/network/updates","dismissConfigurationNoticePath":"/settings/dismiss-notice/dependabot_configuration_notice","configurationNoticeDismissed":null},"displayName":"2024-09-01-Tags-Improvement.md","displayUrl":"https://github.com/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md?raw=true","headerInfo":{"blobSize":"8.62 KB","deleteTooltip":"You must be signed in to make or propose changes","editTooltip":"You must be signed in to make or propose changes","ghDesktopPath":"https://desktop.github.com","isGitLfs":false,"onBranch":true,"shortPath":"9563101","siteNavLoginPath":"/login?return_to=https%3A%2F%2Fgithub.com%2FOAI%2FOpenAPI-Specification%2Fblob%2Fmain%2Fproposals%2F2024-09-01-Tags-Improvement.md","isCSV":false,"isRichtext":true,"lineInfo":{"truncatedLoc":"165","truncatedSloc":"123"},"mode":"file"},"image":false,"isCodeownersFile":null,"isPlain":false,"isValidLegacyIssueTemplate":false,"isIssueTemplate":false,"isDiscussionTemplate":false,"language":"Markdown","languageID":222,"large":false,"planSupportInfo":{"repoIsFork":null,"repoOwnedByCurrentUser":null,"requestFullPath":"/OAI/OpenAPI-Specification/blob/main/proposals/2024-09-01-Tags-Improvement.md","showFreeOrgGatedFeatureMessage":null,"showPlanSupportBanner":null,"upgradeDataAttributes":null,"upgradePath":null},"publishBannersInfo":{"dismissActionNoticePath":"/settings/dismiss-notice/publish_action_from_dockerfile","releasePath":"/OAI/OpenAPI-Specification/releases/new?marketplace=true","showPublishActionBanner":false},"rawBlobUrl":"https://github.com/OAI/OpenAPI-Specification/raw/refs/heads/main/proposals/2024-09-01-Tags-Improvement.md","renderImageOrRaw":false,"shortPath":null,"symbolsEnabled":true,"tabSize":4,"topBannersInfo":{"overridingGlobalFundingFile":false,"globalPreferredFundingPath":null,"showInvalidCitationWarning":false,"citationHelpUrl":"https://docs.github.com/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-citation-files","actionsOnboardingTip":null},"truncated":false,"viewable":true,"workflowRedirectUrl":null},"copilotInfo":null,"copilotAccessAllowed":false,"copilotSpacesEnabled":false,"modelsAccessAllowed":false,"modelsRepoIntegrationEnabled":false,"isMarketplaceEnabled":true},"codeViewBlobLayoutRoute.StyledBlob":{"rawLines":["# Tags Improvement","","","## Metadata","","|Tag |Value |","|---- | ---------------- |","|Proposal |[2024-09-01-Tags-Improvement](https://github.com/OAI/OpenAPI-Specification/tree/main/proposals/{2024-09-01-Tags-Improvement.md})|","|Authors|[Lorna Mitchell](https://github.com/lornajane)|","|Review Manager | TBD |","|Status |Proposal|","|Implementations | |","|Issues | [1367](https://github.com/OAI/OpenAPI-Specification/issues/1367), [2843](https://github.com/OAI/OpenAPI-Specification/issues/2843), |","|Previous Revisions | None, but see [Moonwalk discussion](https://github.com/OAI/sig-moonwalk/discussions/67)","","## Change Log","","|Date |Responsible Party |Description |","|---- | ---------------- | ---------- |","| 2024-09-01 | @lornajane | Initial draft |","","## Introduction","","Evolve the existing `tags` implementation to (optionally) support more use cases, such as giving the tags some grouping/relationships and adding more metadata.","","## Motivation","","The tags feature hasn't changed since the spec was still called Swagger, but it's one of the most-extended aspects of OpenAPI with most tools supporting some sort of grouping or additional metadata. One motivation for this proposal is to \"pave the cowpath\" and formalise some of the patterns from those extensions as part of the specification.","","The existing tags implementation is also quite limiting, so users/tools feel they \"cannot\" use tags, because they are so widely implemented for documentation navigation and required exactly one tag per operation, to be used only for this single purpose or to be opted out using extensions such as `x-traitTag`. The result is that we see lots of extensions that add arbitrary metadata to operations, some of them even become part of the specification officially (looking at you, `deprecated: true`) or being so widely used that we should probably adopt them (`x-internal`, `x-experimental`). The specification does have a way of tagging operations, but it's too limited and the result is that everything has to be added as an extension field.","","On a personal note, I work for a tool vendor and was proposing these changes internally; but the problems affect all OpenAPI users so I brought it to the main project.","","### Supporting evidence","","There are several examples \"in the wild\" of where a better tags implementation would have helped. Here is a selection of publicly-accessible examples to illustrate some of the problems this proposal could help with:","","- Grouping of tags is a very common use case, almost everyone uses some sort of extra hierarchy to group the tags themselves, which makes sense as our APIs are only getting more complex, something like [`x-tagGroups`](https://redocly.com/docs/api-reference-docs/specification-extensions/x-tag-groups/) is a good example - and there's a [very active open issue on OpenAPI specification itself](https://github.com/OAI/OpenAPI-Specification/issues/1367)","- Various tag-alike additions exist, sometimes called \"badges\" or similar; I'd include extensions such as [`x-internal`](https://redocly.com/docs/cli/guides/hide-apis/#step-1-add-x-internal-to-the-api-description) as a tag-alike since they could be tags if more than one tag (or tag type) could be applied.","- Additional display metadata is also in active use in the wild, see [`x-displayName`](https://redocly.com/docs/api-reference-docs/specification-extensions/x-display-name) and this [OpenAPI specification issue](https://github.com/OAI/OpenAPI-Specification/issues/2843)","","## Proposed solution","","Originally proposed in a [Moonwalk discussion](https://github.com/OAI/sig-moonwalk/discussions/67), I am proposing three backwards-compatible additions to the existing tags feature:","","* Tags get a `summary` alongside `name` and `description`. In keeping with our existing practices: name is the identifier, summary is the short display content, and description is available in contexts where more information is appropriate.","* A `parent` field is added to support a hierarchy without adding either separators or a new data type. Your tag can belong to another tag.","* A `kind` field to explain which family of tags this tag belongs to (previously proposed as `type`). We'd expecting these to be `nav`, `badge`, `internal` and probably some other things that other tooling types would find useful.","","An example could look something like this:","","```yaml","tags:","- name: deprecated","  kind: internal","  summary: Deprecated","  description: This operation has been deprecated and will be removed in the future. Avoid using items with this tag.","- name: shop","  kind: nav","  summary: Order Online","  description: Operations relating to the retail operations behind the [online shopping site](https://example.com/shopping).","- name: products","  kind: nav","  parent: shop","  summary: Products","  description: View and manage the product catalog.","- name: orders","  kind: nav","  parent: shop","  summary: Online Orders","  description: Place, fulfil and invoice orders for the online shop.","","```","","Rather than making an allowed list of kinds, we will instead leave that open for user extension and keep a list of the recommended/expected types in a registry and evolve that as conventions emerge.","","## Detailed design","","The following section is an updated specification section, for the top-level tags object only (no other changes are needed):","","---","","#### Tag Object","","Adds metadata to a single tag that is used by the [Operation Object](#operation-object).","Each tag used in the Operation Object instances MAY have a Tag Object defined.","","##### Fixed Fields","","Field Name | Type | Description","---|:---:|---","\u003ca name=\"tagName\"\u003e\u003c/a\u003ename | `string` | **REQUIRED**. The name of the tag. Use this value in the `tags` array of an Operation.","\u003ca name=\"tagSummary\"\u003e\u003c/a\u003esummary | `string` | A short summary of the tag, used for display purposes.","\u003ca name=\"tagDescription\"\u003e\u003c/a\u003edescription | `string` | A description for the tag. [CommonMark syntax](https://spec.commonmark.org/) MAY be used for rich text representation.","\u003ca name=\"tagExternalDocs\"\u003e\u003c/a\u003eexternalDocs | [External Documentation Object](#external-documentation-object) | Additional external documentation for this tag.","\u003ca name=\"tagParent\"\u003e\u003c/a\u003eparent | `string` | The `name` of a tag that this tags is nested under. The named tag MUST exist in the API description, and circular references between parent and child tags MUST NOT be used.","\u003ca name=\"tagKind\"\u003e\u003c/a\u003ekind | `string` | A machine-readable string to categorize what sort of tag it is. Common uses are `nav` for Navigation, `badge` for badges, `internal` for internal APIs, but any string value can be used. A registry of known values is available.","","This object MAY be extended with [Specification Extensions](#specification-extensions).","","##### Tag Object Example","","```json","{","  \"name\": \"account-updates\",","  \"summary\": \"Account Updates\",","  \"description\": \"Account update operations\",","  \"kind\": \"nav\"","},","{","  \"name\": \"partner\",","  \"summary\": \"Partner\",","  \"description\": \"Operations available to the partners network\",","  \"parent\": \"external\",","  \"kind\": \"audience\"","},","{","  \"name\": \"external\",","  \"summary\": \"External\",","  \"description\": \"Operations available to external consumers\",","  \"kind\": \"audience\"","}","```","","```yaml","- name: account-updates","  summary: Account Updates","  description: Account update operations","  kind: nav","","- name: partner","  summary: Partner","  description: Operations available to the partners network","  parent: external","  kind: audience","","- name: external","  summary: External","  description: Operations available to external consumers","  kind: audience","```","","---","","## Backwards compatibility","","All new fields are optional, so existing API descriptions will remain valid and useful.","Some users may wish to adopt some of the following steps on upgrade:","","- Set `kind: nav` if their existing tags are currently used for navigation entries in documentation tooling.","- Change `x-displayName` in `tag` objects to `summary` instead.","- Add a tag to replace each `x-tagGroups` entry, and set the `parent` field for each of the tags in the groups.","- Change `x-badges` extensions to instead be a tag with `kind: badge`.","- Change features like `x-internal` to be a tag with a specific `kind` set. Similarly some lifecycle use cases such as `x-beta` could be replaced with tags.","","## Alternatives considered","","- Continue to use tags as-is, and extend the spec for each use case that users need rather than providing an open metadata implementation.","  We've been slow to iterate and I would rather \"open\" the options than try to control them.","  The API space evolves quite quickly.","","- Set `children` rather than `parent` on the tags and operate a top-down relationship.","  The suggestion of allowing multiple links or a graph approach was also mentioned.","  In both cases, there are good ideas in every direction, but our responsibility is to implement a structure that users can easily understand and maintain."],"stylingDirectives":[[[0,18,"pl-mh"],[2,18,"pl-en"]],[],[],[[0,11,"pl-mh"],[3,11,"pl-en"]],[],[[0,1,"pl-ml"],[5,6,"pl-ml"],[12,13,"pl-ml"]],[[0,1,"pl-ml"],[6,7,"pl-ml"],[25,26,"pl-ml"]],[[0,1,"pl-ml"],[10,11,"pl-ml"],[11,12,"pl-s"],[39,40,"pl-s"],[40,41,"pl-s"],[41,138,"pl-corl"],[138,139,"pl-s"],[139,140,"pl-ml"]],[[0,1,"pl-ml"],[8,9,"pl-ml"],[9,10,"pl-s"],[24,25,"pl-s"],[25,26,"pl-s"],[26,54,"pl-corl"],[54,55,"pl-s"],[55,56,"pl-ml"]],[[0,1,"pl-ml"],[16,17,"pl-ml"],[22,23,"pl-ml"]],[[0,1,"pl-ml"],[8,9,"pl-ml"],[17,18,"pl-ml"]],[[0,1,"pl-ml"],[17,18,"pl-ml"],[19,20,"pl-ml"]],[[0,1,"pl-ml"],[8,9,"pl-ml"],[10,11,"pl-s"],[15,16,"pl-s"],[16,17,"pl-s"],[17,73,"pl-corl"],[73,74,"pl-s"],[76,77,"pl-s"],[81,82,"pl-s"],[82,83,"pl-s"],[83,139,"pl-corl"],[139,140,"pl-s"],[142,143,"pl-ml"]],[[36,37,"pl-s"],[56,57,"pl-s"],[57,58,"pl-s"],[58,108,"pl-corl"],[108,109,"pl-s"]],[],[[0,13,"pl-mh"],[3,13,"pl-en"]],[],[[0,1,"pl-ml"],[6,7,"pl-ml"],[25,26,"pl-ml"],[38,39,"pl-ml"]],[[0,1,"pl-ml"],[6,7,"pl-ml"],[25,26,"pl-ml"],[38,39,"pl-ml"]],[[0,1,"pl-ml"],[13,14,"pl-ml"],[15,25,"pl-s"],[16,25,"pl-corl"],[26,27,"pl-ml"],[42,43,"pl-ml"]],[],[[0,15,"pl-mh"],[3,15,"pl-en"]],[],[[20,21,"pl-s"],[21,25,"pl-c1"],[25,26,"pl-s"]],[],[[0,13,"pl-mh"],[3,13,"pl-en"]],[],[],[],[[297,298,"pl-s"],[298,308,"pl-c1"],[308,309,"pl-s"],[478,479,"pl-s"],[479,495,"pl-c1"],[495,496,"pl-s"],[558,559,"pl-s"],[559,569,"pl-c1"],[569,570,"pl-s"],[572,573,"pl-s"],[573,587,"pl-c1"],[587,588,"pl-s"]],[],[],[],[[0,23,"pl-mh"],[4,23,"pl-en"]],[],[],[],[[0,1,"pl-v"],[202,203,"pl-s"],[203,204,"pl-s"],[204,215,"pl-c1"],[215,216,"pl-s"],[216,217,"pl-s"],[217,218,"pl-s"],[218,300,"pl-corl"],[300,301,"pl-s"],[336,337,"pl-s"],[391,392,"pl-s"],[392,393,"pl-s"],[393,449,"pl-corl"],[449,450,"pl-s"]],[[0,1,"pl-v"],[106,107,"pl-s"],[107,108,"pl-s"],[108,118,"pl-c1"],[118,119,"pl-s"],[119,120,"pl-s"],[120,121,"pl-s"],[121,212,"pl-corl"],[212,213,"pl-s"]],[[0,1,"pl-v"],[69,70,"pl-s"],[70,71,"pl-s"],[71,84,"pl-c1"],[84,85,"pl-s"],[85,86,"pl-s"],[86,87,"pl-s"],[87,170,"pl-corl"],[170,171,"pl-s"],[181,182,"pl-s"],[209,210,"pl-s"],[210,211,"pl-s"],[211,267,"pl-corl"],[267,268,"pl-s"]],[],[[0,20,"pl-mh"],[3,20,"pl-en"]],[],[[25,26,"pl-s"],[45,46,"pl-s"],[46,47,"pl-s"],[47,97,"pl-corl"],[97,98,"pl-s"]],[],[[0,1,"pl-v"],[13,14,"pl-s"],[14,21,"pl-c1"],[21,22,"pl-s"],[33,34,"pl-s"],[34,38,"pl-c1"],[38,39,"pl-s"],[44,45,"pl-s"],[45,56,"pl-c1"],[56,57,"pl-s"]],[[0,1,"pl-v"],[4,5,"pl-s"],[5,11,"pl-c1"],[11,12,"pl-s"]],[[0,1,"pl-v"],[4,5,"pl-s"],[5,9,"pl-c1"],[9,10,"pl-s"],[93,94,"pl-s"],[94,98,"pl-c1"],[98,99,"pl-s"],[129,130,"pl-s"],[130,133,"pl-c1"],[133,134,"pl-s"],[136,137,"pl-s"],[137,142,"pl-c1"],[142,143,"pl-s"],[145,146,"pl-s"],[146,154,"pl-c1"],[154,155,"pl-s"]],[],[],[],[[0,3,"pl-s"],[3,7,"pl-en"]],[[0,4,"pl-ent"]],[[2,6,"pl-ent"],[8,18,"pl-s"]],[[2,6,"pl-ent"],[8,16,"pl-s"]],[[2,9,"pl-ent"],[11,21,"pl-s"]],[[2,13,"pl-ent"],[15,117,"pl-s"]],[[2,6,"pl-ent"],[8,12,"pl-s"]],[[2,6,"pl-ent"],[8,11,"pl-s"]],[[2,9,"pl-ent"],[11,23,"pl-s"]],[[2,13,"pl-ent"],[15,124,"pl-s"]],[[2,6,"pl-ent"],[8,16,"pl-s"]],[[2,6,"pl-ent"],[8,11,"pl-s"]],[[2,8,"pl-ent"],[10,14,"pl-s"]],[[2,9,"pl-ent"],[11,19,"pl-s"]],[[2,13,"pl-ent"],[15,51,"pl-s"]],[[2,6,"pl-ent"],[8,14,"pl-s"]],[[2,6,"pl-ent"],[8,11,"pl-s"]],[[2,8,"pl-ent"],[10,14,"pl-s"]],[[2,9,"pl-ent"],[11,24,"pl-s"]],[[2,13,"pl-ent"],[15,68,"pl-s"]],[],[[0,3,"pl-s"]],[],[],[],[[0,18,"pl-mh"],[3,18,"pl-en"]],[],[],[],[[0,3,"pl-ms"]],[],[[0,15,"pl-mh"],[5,15,"pl-en"]],[],[[50,51,"pl-s"],[67,68,"pl-s"],[68,69,"pl-s"],[69,86,"pl-corl"],[86,87,"pl-s"]],[],[],[[0,18,"pl-mh"],[6,18,"pl-en"]],[],[],[],[[1,2,"pl-ent"],[3,7,"pl-e"],[8,9,"pl-s"],[9,16,"pl-s"],[16,17,"pl-s"],[20,21,"pl-ent"],[29,30,"pl-s"],[30,36,"pl-c1"],[36,37,"pl-s"],[40,42,"pl-s"],[50,52,"pl-s"],[97,98,"pl-s"],[98,102,"pl-c1"],[102,103,"pl-s"]],[[1,2,"pl-ent"],[3,7,"pl-e"],[8,9,"pl-s"],[9,19,"pl-s"],[19,20,"pl-s"],[23,24,"pl-ent"],[35,36,"pl-s"],[36,42,"pl-c1"],[42,43,"pl-s"]],[[1,2,"pl-ent"],[3,7,"pl-e"],[8,9,"pl-s"],[9,23,"pl-s"],[23,24,"pl-s"],[27,28,"pl-ent"],[43,44,"pl-s"],[44,50,"pl-c1"],[50,51,"pl-s"],[81,82,"pl-s"],[99,100,"pl-s"],[100,101,"pl-s"],[101,129,"pl-corl"],[129,130,"pl-s"]],[[1,2,"pl-ent"],[3,7,"pl-e"],[8,9,"pl-s"],[9,24,"pl-s"],[24,25,"pl-s"],[28,29,"pl-ent"],[45,46,"pl-s"],[75,76,"pl-s"],[76,77,"pl-s"],[77,107,"pl-corl"],[107,108,"pl-s"]],[[1,2,"pl-ent"],[3,7,"pl-e"],[8,9,"pl-s"],[9,18,"pl-s"],[18,19,"pl-s"],[22,23,"pl-ent"],[33,34,"pl-s"],[34,40,"pl-c1"],[40,41,"pl-s"],[48,49,"pl-s"],[49,53,"pl-c1"],[53,54,"pl-s"]],[[1,2,"pl-ent"],[3,7,"pl-e"],[8,9,"pl-s"],[9,16,"pl-s"],[16,17,"pl-s"],[20,21,"pl-ent"],[29,30,"pl-s"],[30,36,"pl-c1"],[36,37,"pl-s"],[120,121,"pl-s"],[121,124,"pl-c1"],[124,125,"pl-s"],[142,143,"pl-s"],[143,148,"pl-c1"],[148,149,"pl-s"],[162,163,"pl-s"],[163,171,"pl-c1"],[171,172,"pl-s"]],[],[[33,34,"pl-s"],[58,59,"pl-s"],[59,60,"pl-s"],[60,85,"pl-corl"],[85,86,"pl-s"]],[],[[0,24,"pl-mh"],[6,24,"pl-en"]],[],[[0,3,"pl-s"],[3,7,"pl-en"]],[],[[2,8,"pl-ent"],[10,27,"pl-s"],[10,11,"pl-pds"],[26,27,"pl-pds"]],[[2,11,"pl-ent"],[13,30,"pl-s"],[13,14,"pl-pds"],[29,30,"pl-pds"]],[[2,15,"pl-ent"],[17,44,"pl-s"],[17,18,"pl-pds"],[43,44,"pl-pds"]],[[2,8,"pl-ent"],[10,15,"pl-s"],[10,11,"pl-pds"],[14,15,"pl-pds"]],[],[],[[2,8,"pl-ent"],[10,19,"pl-s"],[10,11,"pl-pds"],[18,19,"pl-pds"]],[[2,11,"pl-ent"],[13,22,"pl-s"],[13,14,"pl-pds"],[21,22,"pl-pds"]],[[2,15,"pl-ent"],[17,63,"pl-s"],[17,18,"pl-pds"],[62,63,"pl-pds"]],[[2,10,"pl-ent"],[12,22,"pl-s"],[12,13,"pl-pds"],[21,22,"pl-pds"]],[[2,8,"pl-ent"],[10,20,"pl-s"],[10,11,"pl-pds"],[19,20,"pl-pds"]],[],[],[[2,8,"pl-ent"],[10,20,"pl-s"],[10,11,"pl-pds"],[19,20,"pl-pds"]],[[2,11,"pl-ent"],[13,23,"pl-s"],[13,14,"pl-pds"],[22,23,"pl-pds"]],[[2,15,"pl-ent"],[17,61,"pl-s"],[17,18,"pl-pds"],[60,61,"pl-pds"]],[[2,8,"pl-ent"],[10,20,"pl-s"],[10,11,"pl-pds"],[19,20,"pl-pds"]],[],[[0,3,"pl-s"]],[],[[0,3,"pl-s"],[3,7,"pl-en"]],[[2,6,"pl-ent"],[8,23,"pl-s"]],[[2,9,"pl-ent"],[11,26,"pl-s"]],[[2,13,"pl-ent"],[15,40,"pl-s"]],[[2,6,"pl-ent"],[8,11,"pl-s"]],[],[[2,6,"pl-ent"],[8,15,"pl-s"]],[[2,9,"pl-ent"],[11,18,"pl-s"]],[[2,13,"pl-ent"],[15,59,"pl-s"]],[[2,8,"pl-ent"],[10,18,"pl-s"]],[[2,6,"pl-ent"],[8,16,"pl-s"]],[],[[2,6,"pl-ent"],[8,16,"pl-s"]],[[2,9,"pl-ent"],[11,19,"pl-s"]],[[2,13,"pl-ent"],[15,57,"pl-s"]],[[2,6,"pl-ent"],[8,16,"pl-s"]],[[0,3,"pl-s"],[0,1,"pl-pds"],[1,2,"pl-pds"],[2,3,"pl-pds"]],[[0,0,"pl-s"]],[[0,3,"pl-s"]],[[0,0,"pl-s"]],[[0,26,"pl-s"]],[[0,0,"pl-s"]],[[0,87,"pl-s"]],[[0,68,"pl-s"]],[[0,0,"pl-s"]],[[0,7,"pl-s"],[6,7,"pl-pds"],[7,108,"pl-s"]],[[2,63,"pl-s"]],[[2,111,"pl-s"]],[[2,61,"pl-ent"],[63,70,"pl-s"]],[[2,156,"pl-s"]],[],[[0,26,"pl-c"],[0,1,"pl-c"]],[],[[2,138,"pl-s"]],[[2,92,"pl-s"]],[[2,38,"pl-s"]],[],[[2,86,"pl-s"]],[[2,83,"pl-s"]],[[2,155,"pl-s"]],[]],"colorizedLines":null}},"title":"OpenAPI-Specification/proposals/2024-09-01-Tags-Improvement.md at main · OAI/OpenAPI-Specification","appPayload":{},"meta":{"title":"OpenAPI-Specification/proposals/2024-09-01-Tags-Improvement.md at main · OAI/OpenAPI-Specification"}}</script>
  <div data-target="react-app.reactRoot"><meta name="github-code-view-meta-stats" id="github-code-view-meta-stats" data-hydrostats="publish"/> <!-- --> <a hidden="" id="code-view-repo-link" href="/OAI/OpenAPI-Specification" data-discover="true"></a> <div class="d-none"></div><div><div style="--spacing:var(--spacing-none)" class="prc-PageLayout-PageLayoutRoot--KH-d" data-component="SplitPageLayout" data-has-sidebar="true"><div class="prc-PageLayout-SidebarWrapper-kLG4B CopilotSidePanelSidebar-module__SidePanel__L3O0C CopilotSidePanelSidebar-module__HiddenSidePanel__TBRGn" style="--spacing-column:var(--spacing-none)" data-is-hidden="false" data-position="end" data-sticky="true" data-responsive-variant="fullscreen"><div class="prc-PageLayout-VerticalDivider-9QRmK prc-PageLayout-SidebarVerticalDivider-0Rl0V" data-component="PageLayout.VerticalDivider" data-variant="line" data-position="end" style="--spacing:var(--spacing-none)"><div class="prc-PageLayout-DraggableHandle-9s6B4" data-component="PageLayout.DragHandle" role="slider" aria-label="Draggable pane splitter" aria-valuemin="450" aria-valuemax="768" aria-valuenow="544" aria-valuetext="Pane width 544 pixels" tabindex="0"></div></div><div class="prc-PageLayout-Sidebar-iciWg" data-component="SplitPageLayout.Sidebar" data-resizable="true" style="--spacing:var(--spacing-normal);--pane-min-width:450px;--pane-max-width:768px;--pane-width-custom:544px;--pane-width-size:var(--pane-width-custom);--pane-width:544px"><div class="height-full"><div id="copilot-side-panel-content" class="height-full"></div></div></div></div><div class="prc-PageLayout-PageLayoutWrapper-2BhU2" data-width="full"><div class="prc-PageLayout-PageLayoutContent-BneH9"><div class="CodeViewFileTreeLayout-module__sidebar__n_Aau" tabindex="0"><div class="prc-PageLayout-PaneWrapper-pHPop ReposFileTreePane-module__Pane__rBZpI ReposFileTreePane-module__HideTree__AYZnm ReposFileTreePane-module__HidePane__VHAVt" style="--offset-header:0px;--spacing-row:var(--spacing-none);--spacing-column:var(--spacing-none)" data-is-hidden="false" data-position="start" data-sticky="true"><div class="prc-PageLayout-HorizontalDivider-JLVqp prc-PageLayout-PaneHorizontalDivider-9tbnE" data-component="PageLayout.HorizontalDivider" data-variant-regular="none" data-variant-narrow="none" data-position="start" style="--spacing-divider:var(--spacing-none);--spacing:var(--spacing-none)"></div><div class="prc-PageLayout-Pane-AyzHK" data-component="SplitPageLayout.Pane" data-resizable="true" style="--spacing:var(--spacing-none);--pane-min-width:256px;--pane-max-width:calc(100vw - var(--pane-max-width-diff));--pane-width-size:var(--pane-width-large);--pane-width:320px"></div><div class="prc-PageLayout-VerticalDivider-9QRmK prc-PageLayout-PaneVerticalDivider-le57g" data-component="PageLayout.VerticalDivider" data-variant-narrow="none" data-variant-regular="line" data-variant-wide="line" data-position="start" style="--spacing:var(--spacing-none)"><div class="prc-PageLayout-DraggableHandle-9s6B4" data-component="PageLayout.DragHandle" role="slider" aria-label="Draggable pane splitter" aria-valuemin="256" aria-valuemax="600" aria-valuenow="320" aria-valuetext="Pane width 320 pixels" tabindex="0"></div></div></div></div><div data-component="SplitPageLayout.Content" class="prc-PageLayout-ContentWrapper-gR9eG"><div class="prc-PageLayout-Content-xWL-A" data-width="full" style="--spacing:var(--spacing-none)"><div class="SharedPageLayout-module__content__IwGAp" data-selector="repos-split-pane-content" tabindex="0"> <!-- --> <div class="container CodeViewHeader-module__Box__JkPOb"><div class="CodeViewHeader-module__StickyHeader__Qn7UN" id="StickyHeader"><div class="CodeViewHeader-module__Box_1__SbNDV"><div class="CodeViewHeader-module__Box_2__TB46f"><div class="react-code-view-header-wrap--narrow CodeViewHeader-module__Box_3__q1zUL"><div class="CodeViewHeader-module__treeToggleWrapper__RQ__9"><h2 class="use-tree-pane-module__Heading__s4QbZ prc-Heading-Heading-MtWFE" data-component="Heading"><button data-component="Button" type="button" aria-label="Expand file tree" data-testid="expand-file-tree-button-mobile" class="prc-Button-ButtonBase-9n-Xk ExpandFileTreeButton-module__Button_1__Svs95" data-loading="false" data-size="medium" data-variant="invisible"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="leadingVisual" class="prc-Button-Visual-YNt2F prc-Button-VisualWrap-E4cnq"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-arrow-left" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M7.78 12.53a.75.75 0 0 1-1.06 0L2.47 8.28a.75.75 0 0 1 0-1.06l4.25-4.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L4.81 7h7.44a.75.75 0 0 1 0 1.5H4.81l2.97 2.97a.75.75 0 0 1 0 1.06Z"></path></svg></span><span data-component="text" class="prc-Button-Label-FWkx3">Files</span></span></button><button data-component="IconButton" type="button" data-testid="expand-file-tree-button" aria-controls="repos-file-tree" class="prc-Button-ButtonBase-9n-Xk position-relative ExpandFileTreeButton-module__expandButton__hDOcv ExpandFileTreeButton-module__filesButtonBreakpoint__zEvz3 fgColor-muted prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="medium" data-variant="invisible" aria-labelledby="_R_15daidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-sidebar-collapse" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M6.823 7.823a.25.25 0 0 1 0 .354l-2.396 2.396A.25.25 0 0 1 4 10.396V5.604a.25.25 0 0 1 .427-.177Z"></path><path d="M1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0ZM1.5 1.75v12.5c0 .138.112.25.25.25H9.5v-13H1.75a.25.25 0 0 0-.25.25ZM11 14.5h3.25a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25H11Z"></path></svg></button><span class="prc-TooltipV2-Tooltip-tLeuB" data-direction="se" data-component="Tooltip" aria-hidden="true" id="_R_15daidek5_">Expand file tree</span><div class="d-none"></div></h2></div><div class="react-code-view-header-mb--narrow mr-2"><button data-component="Button" type="button" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-label="main branch" data-testid="anchor-button" data-icv-name="Switch branches/tags" class="prc-Button-ButtonBase-9n-Xk ref-selector-class RefSelectorAnchoredOverlay-module__RefSelectorOverlayBtn__a3WK3" data-loading="false" data-size="medium" data-variant="default" id="ref-picker-repos-header-ref-selector-wide"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="text" class="prc-Button-Label-FWkx3"><div class="RefSelectorAnchoredOverlay-module__RefSelectorOverlayContainer__yaf4p"><div class="RefSelectorAnchoredOverlay-module__RefSelectorOverlayHeader__XtXRG"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-git-branch" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25Zm-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z"></path></svg></div><div style="max-width:125px" class="ref-selector-button-text-container RefSelectorAnchoredOverlay-module__RefSelectorBtnTextContainer__Di3rk"><span class="RefSelectorAnchoredOverlay-module__RefSelectorText__w_fmP"> <!-- -->main</span></div></div></span><span data-component="trailingVisual" class="prc-Button-Visual-YNt2F prc-Button-VisualWrap-E4cnq"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-triangle-down" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="m4.427 7.427 3.396 3.396a.25.25 0 0 0 .354 0l3.396-3.396A.25.25 0 0 0 11.396 7H4.604a.25.25 0 0 0-.177.427Z"></path></svg></span></span></button><div class="d-none"></div></div><div class="react-code-view-header-mb--narrow CodeViewHeader-module__Box_5__MQ0hL"><div class="Breadcrumb-module__container__Vxvev Breadcrumb-module__lg__Rjz0A"><nav data-testid="breadcrumbs" aria-labelledby="repos-header-breadcrumb-heading" id="repos-header-breadcrumb" class="Breadcrumb-module__nav__rQFDj"><h2 class="sr-only ScreenReaderHeading-module__userSelectNone__rwWIk prc-Heading-Heading-MtWFE" data-component="Heading" data-testid="screen-reader-heading" id="repos-header-breadcrumb-heading">Breadcrumbs</h2><ol class="Breadcrumb-module__list__ZH6zr"><li class="Breadcrumb-module__listItem__Ib0x_"><a class="Breadcrumb-module__repoLink__O2Nbs prc-Link-Link-9ZwDx" data-component="Link" data-testid="breadcrumbs-repo-link" href="/OAI/OpenAPI-Specification/tree/main" data-discover="true">OpenAPI-Specification</a></li><li class="Breadcrumb-module__listItem__Ib0x_"><span class="Breadcrumb-module__separator__eNwsI Breadcrumb-module__lg__Rjz0A" aria-hidden="true">/</span><a class="Breadcrumb-module__directoryLink__kQy_t prc-Link-Link-9ZwDx" data-component="Link" href="/OAI/OpenAPI-Specification/tree/main/proposals" data-discover="true">proposals</a></li></ol></nav><div data-testid="breadcrumbs-filename" class="Breadcrumb-module__filename__equZR"><span class="Breadcrumb-module__separator__eNwsI Breadcrumb-module__lg__Rjz0A" aria-hidden="true">/</span><h1 class="Breadcrumb-module__filenameHeading__MNMtw Breadcrumb-module__lg__Rjz0A prc-Heading-Heading-MtWFE" data-component="Heading" tabindex="-1" id="file-name-id">2024-09-01-Tags-Improvement.md</h1></div><button data-component="IconButton" type="button" class="prc-Button-ButtonBase-9n-Xk ml-2 prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="small" data-variant="invisible" aria-labelledby="_R_1tdaidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-copy" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></button><span class="CopyToClipboardButton-module__tooltip__BhMvU prc-TooltipV2-Tooltip-tLeuB" data-direction="nw" data-component="Tooltip" aria-label="Copy path" aria-hidden="true" id="_R_1tdaidek5_">Copy path</span></div></div></div><div class="react-code-view-header-element--wide"><div class="CodeViewHeader-module__Box_7___0R6c"><div class="d-flex gap-2"><div><div class="CodeViewHeader-module__FileResultsList__JDzUy"><span class="d-flex FileResultsList-module__FilesSearchBox__ivVkc TextInput-wrapper prc-components-TextInputWrapper-Hpdqi prc-components-TextInputBaseWrapper-wY-n0" data-no-trailing-action="true" data-component="TextInput" data-leading-visual="true" data-trailing-visual="true" aria-busy="false"><span class="TextInput-icon" id="_R_1cmdaidek5_" aria-hidden="true" data-component="TextInput.LeadingVisual"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-search" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M10.68 11.74a6 6 0 0 1-7.922-8.982 6 6 0 0 1 8.982 7.922l3.04 3.04a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215ZM11.5 7a4.499 4.499 0 1 0-8.997 0A4.499 4.499 0 0 0 11.5 7Z"></path></svg></span><input type="text" aria-label="Go to file" role="combobox" aria-controls="file-results-list" aria-expanded="false" aria-haspopup="dialog" autoCorrect="off" spellCheck="false" placeholder="Go to file" aria-describedby="_R_1cmdaidek5_ _R_1cmdaidek5H1_" data-component="input" class="prc-components-Input-IwWrt" value=""/><span class="TextInput-icon" id="_R_1cmdaidek5H1_" aria-hidden="true" data-component="TextInput.TrailingVisual"></span></span></div><div class="d-none"></div></div><button data-component="Button" type="button" style="display:none" class="prc-Button-ButtonBase-9n-Xk NavigationMenu-module__Button__LpKgm" data-loading="false" data-no-visuals="true" data-size="medium" data-variant="default"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="text" class="prc-Button-Label-FWkx3">Blame</span></span></button><div class="d-none"></div><button data-component="IconButton" type="button" data-testid="more-file-actions-button-nav-menu-wide" aria-haspopup="true" aria-expanded="false" tabindex="0" class="prc-Button-ButtonBase-9n-Xk js-blob-dropdown-click NavigationMenu-module__IconButton__HpX3G prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="medium" data-variant="default" aria-labelledby="_R_7p6daidek5_" id="_R_96daidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-kebab-horizontal" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg></button><span class="prc-TooltipV2-Tooltip-tLeuB" data-direction="nw" data-component="Tooltip" aria-hidden="true" id="_R_7p6daidek5_">More file actions</span></div></div></div><div class="react-code-view-header-element--narrow"><div class="CodeViewHeader-module__Box_7___0R6c"><div class="d-flex gap-2"><button data-component="Button" type="button" style="display:none" class="prc-Button-ButtonBase-9n-Xk NavigationMenu-module__Button__LpKgm" data-loading="false" data-no-visuals="true" data-size="medium" data-variant="default"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="text" class="prc-Button-Label-FWkx3">Blame</span></span></button><div class="d-none"></div><button data-component="IconButton" type="button" data-testid="more-file-actions-button-nav-menu-narrow" aria-haspopup="true" aria-expanded="false" tabindex="0" class="prc-Button-ButtonBase-9n-Xk js-blob-dropdown-click NavigationMenu-module__IconButton__HpX3G prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="medium" data-variant="default" aria-labelledby="_R_7p7daidek5_" id="_R_97daidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-kebab-horizontal" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg></button><span class="prc-TooltipV2-Tooltip-tLeuB" data-direction="nw" data-component="Tooltip" aria-hidden="true" id="_R_7p7daidek5_">More file actions</span></div></div></div></div></div></div></div><div class="CodeView-module__contentWrapper__cG2JH"><div class="react-code-view-bottom-padding"><div class="BlobTopBanners-module__Box__v_nvx"></div></div> <div class="d-none"></div><div class="d-flex flex-column border rounded-2 tmp-mb-3 pl-1"><div class="LatestCommit-module__Box__B25ZT"><h2 class="sr-only ScreenReaderHeading-module__userSelectNone__rwWIk prc-Heading-Heading-MtWFE" data-component="Heading" data-testid="screen-reader-heading">Latest commit</h2><div style="width:120px" class="Skeleton Skeleton--text" data-testid="loading"> </div><div class="d-flex flex-shrink-0 gap-2"><div data-testid="latest-commit-details" class="d-none d-sm-flex flex-items-center"></div><div class="d-flex gap-2"><h2 class="sr-only ScreenReaderHeading-module__userSelectNone__rwWIk prc-Heading-Heading-MtWFE" data-component="Heading" data-testid="screen-reader-heading">History</h2><a data-component="LinkButton" href="/OAI/OpenAPI-Specification/commits/main/proposals/2024-09-01-Tags-Improvement.md" class="prc-Button-ButtonBase-9n-Xk d-none d-lg-flex LinkButton-module__linkButton__nFnov flex-items-center fgColor-default" data-loading="false" data-size="small" data-variant="invisible"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="leadingVisual" class="prc-Button-Visual-YNt2F prc-Button-VisualWrap-E4cnq"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-history" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="m.427 1.927 1.215 1.215a8.002 8.002 0 1 1-1.6 5.685.75.75 0 1 1 1.493-.154 6.5 6.5 0 1 0 1.18-4.458l1.358 1.358A.25.25 0 0 1 3.896 6H.25A.25.25 0 0 1 0 5.75V2.104a.25.25 0 0 1 .427-.177ZM7.75 4a.75.75 0 0 1 .75.75v2.992l2.028.812a.75.75 0 0 1-.557 1.392l-2.5-1A.751.751 0 0 1 7 8.25v-3.5A.75.75 0 0 1 7.75 4Z"></path></svg></span><span data-component="text" class="prc-Button-Label-FWkx3"><span class="fgColor-default">History</span></span></span></a><div class="d-sm-none"></div><div class="d-flex d-lg-none"><a data-component="LinkButton" aria-label="View commit history for this file." href="/OAI/OpenAPI-Specification/commits/main/proposals/2024-09-01-Tags-Improvement.md" class="prc-Button-ButtonBase-9n-Xk LinkButton-module__linkButton__nFnov flex-items-center fgColor-default" data-loading="false" data-size="small" data-variant="invisible" aria-describedby="_R_15lalaidek5_"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="leadingVisual" class="prc-Button-Visual-YNt2F prc-Button-VisualWrap-E4cnq"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-history" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="m.427 1.927 1.215 1.215a8.002 8.002 0 1 1-1.6 5.685.75.75 0 1 1 1.493-.154 6.5 6.5 0 1 0 1.18-4.458l1.358 1.358A.25.25 0 0 1 3.896 6H.25A.25.25 0 0 1 0 5.75V2.104a.25.25 0 0 1 .427-.177ZM7.75 4a.75.75 0 0 1 .75.75v2.992l2.028.812a.75.75 0 0 1-.557 1.392l-2.5-1A.751.751 0 0 1 7 8.25v-3.5A.75.75 0 0 1 7.75 4Z"></path></svg></span></span></a><span class="prc-TooltipV2-Tooltip-tLeuB" data-direction="s" data-component="Tooltip" role="tooltip" aria-hidden="true" id="_R_15lalaidek5_">History</span></div></div></div></div></div><div class="d-flex flex-row"><div class="container BlobViewContent-module__blobContainer__DtH2d"><div class="react-code-size-details-banner BlobViewContent-module__codeSizeDetails__e5sUw"><div class="react-code-size-details-banner CodeSizeDetails-module__Box__VcD6l"><div class="text-mono CodeSizeDetails-module__Box_1__GVxQL"><div data-testid="blob-size" class="CodeSizeDetails-module__Truncate_1__lE93V prc-Truncate-Truncate-2G1eo" data-inline="true" title="8.62 KB" style="--truncate-max-width:100%"><span>165 lines (123 loc) · 8.62 KB</span></div></div></div></div><div class="react-blob-view-header-sticky BlobViewContent-module__stickyHeader__VwxB5" id="repos-sticky-header"><div class="BlobViewHeader-module__Box__yhm9u"><div class="react-blob-sticky-header"><div class="FileNameStickyHeader-module__outerWrapper__ZL4Xc FileNameStickyHeader-module__outerWrapperHidden__Zpynk"><div class="FileNameStickyHeader-module__Box_1__Hazu5"><div class="FileNameStickyHeader-module__Box_2__hoolP"><div class="FileNameStickyHeader-module__Box_3__MVKsk"><button data-component="Button" type="button" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-label="main branch" data-testid="anchor-button" data-icv-name="Switch branches/tags" class="prc-Button-ButtonBase-9n-Xk ref-selector-class RefSelectorAnchoredOverlay-module__RefSelectorOverlayBtn__a3WK3" data-loading="false" data-size="medium" data-variant="default" id="ref-picker-repos-header-ref-selector"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="text" class="prc-Button-Label-FWkx3"><div class="RefSelectorAnchoredOverlay-module__RefSelectorOverlayContainer__yaf4p"><div class="RefSelectorAnchoredOverlay-module__RefSelectorOverlayHeader__XtXRG"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-git-branch" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25Zm-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z"></path></svg></div><div style="max-width:125px" class="ref-selector-button-text-container RefSelectorAnchoredOverlay-module__RefSelectorBtnTextContainer__Di3rk"><span class="RefSelectorAnchoredOverlay-module__RefSelectorText__w_fmP"> <!-- -->main</span></div></div></span><span data-component="trailingVisual" class="prc-Button-Visual-YNt2F prc-Button-VisualWrap-E4cnq"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-triangle-down" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="m4.427 7.427 3.396 3.396a.25.25 0 0 0 .354 0l3.396-3.396A.25.25 0 0 0 11.396 7H4.604a.25.25 0 0 0-.177.427Z"></path></svg></span></span></button><div class="d-none"></div></div><div class="FileNameStickyHeader-module__Box_4__FLhtt"><div class="Breadcrumb-module__container__Vxvev Breadcrumb-module__md__Wb1Gs"><nav data-testid="breadcrumbs" aria-labelledby="sticky-breadcrumb-heading" id="sticky-breadcrumb" class="Breadcrumb-module__nav__rQFDj"><h2 class="sr-only ScreenReaderHeading-module__userSelectNone__rwWIk prc-Heading-Heading-MtWFE" data-component="Heading" data-testid="screen-reader-heading" id="sticky-breadcrumb-heading">Breadcrumbs</h2><ol class="Breadcrumb-module__list__ZH6zr"><li class="Breadcrumb-module__listItem__Ib0x_"><a class="Breadcrumb-module__repoLink__O2Nbs prc-Link-Link-9ZwDx" data-component="Link" data-testid="breadcrumbs-repo-link" href="/OAI/OpenAPI-Specification/tree/main" data-discover="true">OpenAPI-Specification</a></li><li class="Breadcrumb-module__listItem__Ib0x_"><span class="Breadcrumb-module__separator__eNwsI Breadcrumb-module__md__Wb1Gs" aria-hidden="true">/</span><a class="Breadcrumb-module__directoryLink__kQy_t prc-Link-Link-9ZwDx" data-component="Link" href="/OAI/OpenAPI-Specification/tree/main/proposals" data-discover="true">proposals</a></li></ol></nav><div data-testid="breadcrumbs-filename" class="Breadcrumb-module__filename__equZR"><span class="Breadcrumb-module__separator__eNwsI Breadcrumb-module__md__Wb1Gs" aria-hidden="true">/</span><h1 class="Breadcrumb-module__filenameHeading__MNMtw Breadcrumb-module__md__Wb1Gs prc-Heading-Heading-MtWFE" data-component="Heading" tabindex="-1" id="sticky-file-name-id">2024-09-01-Tags-Improvement.md</h1></div><button data-component="IconButton" type="button" class="prc-Button-ButtonBase-9n-Xk ml-2 prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="small" data-variant="invisible" aria-labelledby="_R_1tb6alaidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-copy" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></button><span class="CopyToClipboardButton-module__tooltip__BhMvU prc-TooltipV2-Tooltip-tLeuB" data-direction="s" data-component="Tooltip" aria-label="Copy path" aria-hidden="true" id="_R_1tb6alaidek5_">Copy path</span></div></div></div><button data-component="Button" type="button" class="prc-Button-ButtonBase-9n-Xk FileNameStickyHeader-module__Button__LSEU_ FileNameStickyHeader-module__GoToTopButton__nxAFn" data-loading="false" data-size="small" data-variant="invisible"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="leadingVisual" class="prc-Button-Visual-YNt2F prc-Button-VisualWrap-E4cnq"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-arrow-up" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M3.47 7.78a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0l4.25 4.25a.751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018L9 4.81v7.44a.75.75 0 0 1-1.5 0V4.81L4.53 7.78a.75.75 0 0 1-1.06 0Z"></path></svg></span><span data-component="text" class="prc-Button-Label-FWkx3">Top</span></span></button></div></div></div><div class="BlobViewHeader-module__Box_1__VEmuQ"><h2 class="sr-only ScreenReaderHeading-module__userSelectNone__rwWIk prc-Heading-Heading-MtWFE" data-component="Heading" data-testid="screen-reader-heading">File metadata and controls</h2><div class="BlobViewHeader-module__Box_2__icUs2"><ul aria-label="File view" class="prc-SegmentedControl-SegmentedControl-lqIXp BlobTabButtons-module__SegmentedControl__jen2u" data-variant="default" data-size="small" data-component="SegmentedControl"><li class="prc-SegmentedControl-Item-tSCQh" data-selected="" data-component="SegmentedControl.Button"><button aria-current="true" class="prc-SegmentedControl-Button-E48xz" type="button" style="--separator-color:transparent"><span class="prc-SegmentedControl-Content-1COlk segmentedControl-content"><div class="prc-SegmentedControl-Text-7S2y2 segmentedControl-text" data-text="Preview">Preview</div></span></button></li><li class="prc-SegmentedControl-Item-tSCQh" data-component="SegmentedControl.Button"><button aria-current="false" class="prc-SegmentedControl-Button-E48xz" type="button" style="--separator-color:var(--borderColor-default)"><span class="prc-SegmentedControl-Content-1COlk segmentedControl-content"><div class="prc-SegmentedControl-Text-7S2y2 segmentedControl-text" data-text="Code">Code</div></span></button></li><li class="prc-SegmentedControl-Item-tSCQh" data-component="SegmentedControl.Button"><button aria-current="false" class="prc-SegmentedControl-Button-E48xz" type="button" style="--separator-color:var(--borderColor-default)"><span class="prc-SegmentedControl-Content-1COlk segmentedControl-content"><div class="prc-SegmentedControl-Text-7S2y2 segmentedControl-text" data-text="Blame">Blame</div></span></button></li></ul><div class="d-none"></div><div class="react-code-size-details-in-header CodeSizeDetails-module__Box__VcD6l"><div class="text-mono CodeSizeDetails-module__Box_1__GVxQL"><div data-testid="blob-size" class="CodeSizeDetails-module__Truncate_1__lE93V prc-Truncate-Truncate-2G1eo" data-inline="true" title="8.62 KB" style="--truncate-max-width:100%"><span>165 lines (123 loc) · 8.62 KB</span></div></div></div></div><div class="BlobViewHeader-module__Box_3__ng6v2"><div class="d-none"></div><div class="react-blob-header-edit-and-raw-actions BlobViewHeader-module__Box_4__J4Y4W"><div class="d-none"></div><div class="prc-ButtonGroup-ButtonGroup-vFUrY" data-component="ButtonGroup"><div class="prc-ButtonGroup-Item-PqvDl"><a data-component="LinkButton" href="https://github.com/OAI/OpenAPI-Specification/raw/refs/heads/main/proposals/2024-09-01-Tags-Improvement.md" data-testid="raw-button" class="prc-Button-ButtonBase-9n-Xk LinkButton-module__linkButton__nFnov BlobViewHeader-module__LinkButton__X9kx2" data-loading="false" data-no-visuals="true" data-size="small" data-variant="default"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-Iohp5"><span data-component="text" class="prc-Button-Label-FWkx3">Raw</span></span></a></div><div class="prc-ButtonGroup-Item-PqvDl"><button data-component="IconButton" type="button" data-testid="copy-raw-button" class="prc-Button-ButtonBase-9n-Xk prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="small" data-variant="default" aria-labelledby="_R_6inj6alaidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-copy" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></button><span class="prc-TooltipV2-Tooltip-tLeuB" data-direction="n" data-component="Tooltip" aria-hidden="true" id="_R_6inj6alaidek5_">Copy raw file</span></div><div class="prc-ButtonGroup-Item-PqvDl"><button data-component="IconButton" type="button" data-testid="download-raw-button" class="prc-Button-ButtonBase-9n-Xk BlobViewHeader-module__downloadButton__ef459 prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="small" data-variant="default" aria-labelledby="_R_3inj6alaidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-download" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M2.75 14A1.75 1.75 0 0 1 1 12.25v-2.5a.75.75 0 0 1 1.5 0v2.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 1.5 0v2.5A1.75 1.75 0 0 1 13.25 14Z"></path><path d="M7.25 7.689V2a.75.75 0 0 1 1.5 0v5.689l1.97-1.969a.749.749 0 1 1 1.06 1.06l-3.25 3.25a.749.749 0 0 1-1.06 0L4.22 6.78a.749.749 0 1 1 1.06-1.06l1.97 1.969Z"></path></svg></button><span class="prc-TooltipV2-Tooltip-tLeuB" data-direction="n" data-component="Tooltip" aria-hidden="true" id="_R_3inj6alaidek5_">Download raw file</span></div></div></div><button data-component="IconButton" type="button" aria-pressed="false" class="prc-Button-ButtonBase-9n-Xk tmp-mr-2 TableOfContents-module__IconButton__jrlNM prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="small" data-variant="invisible" aria-labelledby="_R_vj6alaidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-list-unordered" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M5.75 2.5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5ZM2 14a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-6a1 1 0 1 1-2 0 1 1 0 0 1 2 0ZM2 4a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg></button><span class="prc-TooltipV2-Tooltip-tLeuB" data-direction="n" data-component="Tooltip" aria-hidden="true" id="_R_vj6alaidek5_">Outline</span><div class="react-blob-header-edit-and-raw-actions-combined"><button data-component="IconButton" type="button" title="More file actions" data-testid="more-file-actions-button" aria-haspopup="true" aria-expanded="false" tabindex="0" class="prc-Button-ButtonBase-9n-Xk js-blob-dropdown-click BlobViewHeader-module__IconButton__XrMQY prc-Button-IconButton-fyge7" data-loading="false" data-no-visuals="true" data-size="small" data-variant="invisible" aria-labelledby="_R_3t3j6alaidek5_" id="_R_53j6alaidek5_"><svg data-component="Octicon" aria-hidden="true" focusable="false" class="octicon octicon-kebab-horizontal" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg></button><span class="prc-TooltipV2-Tooltip-tLeuB" data-direction="nw" data-component="Tooltip" aria-hidden="true" id="_R_3t3j6alaidek5_">Edit and raw actions</span></div></div></div></div><div></div></div><div class="BlobViewContent-module__blobContentWrapper__JS0W6"><section aria-labelledby="file-name-id-wide file-name-id-mobile" class="BlobContent-module__blobContentSection__VOgZq BlobContent-module__blobContentSectionMarkdown__mPLOK" style="margin-top:46px"><div class="js-snippet-clipboard-copy-unpositioned BlobContent-module__markdownBlob__T8jpG" data-hpc="true" containertiming="hpc"><article class="markdown-body entry-content container-lg" itemprop="text"><div class="markdown-heading" dir="auto"><h1 tabindex="-1" class="heading-element" dir="auto">Tags Improvement</h1><a id="user-content-tags-improvement" class="anchor" aria-label="Permalink: Tags Improvement" href="#tags-improvement"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<div class="markdown-heading" dir="auto"><h2 tabindex="-1" class="heading-element" dir="auto">Metadata</h2><a id="user-content-metadata" class="anchor" aria-label="Permalink: Metadata" href="#metadata"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<markdown-accessiblity-table><table>
<thead>
<tr>
<th>Tag</th>
<th>Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>Proposal</td>
<td><a href="https://github.com/OAI/OpenAPI-Specification/tree/main/proposals/%7B2024-09-01-Tags-Improvement.md%7D">2024-09-01-Tags-Improvement</a></td>
</tr>
<tr>
<td>Authors</td>
<td><a href="https://github.com/lornajane">Lorna Mitchell</a></td>
</tr>
<tr>
<td>Review Manager</td>
<td>TBD</td>
</tr>
<tr>
<td>Status</td>
<td>Proposal</td>
</tr>
<tr>
<td>Implementations</td>
<td></td>
</tr>
<tr>
<td>Issues</td>
<td><a href="https://github.com/OAI/OpenAPI-Specification/issues/1367" data-hovercard-type="issue" data-hovercard-url="/OAI/OpenAPI-Specification/issues/1367/hovercard">1367</a>, <a href="https://github.com/OAI/OpenAPI-Specification/issues/2843" data-hovercard-type="issue" data-hovercard-url="/OAI/OpenAPI-Specification/issues/2843/hovercard">2843</a>,</td>
</tr>
<tr>
<td>Previous Revisions</td>
<td>None, but see <a href="https://github.com/OAI/sig-moonwalk/discussions/67" data-hovercard-type="discussion" data-hovercard-url="/OAI/sig-moonwalk/discussions/67/hovercard">Moonwalk discussion</a></td>
</tr>
</tbody>
</table></markdown-accessiblity-table>
<div class="markdown-heading" dir="auto"><h2 tabindex="-1" class="heading-element" dir="auto">Change Log</h2><a id="user-content-change-log" class="anchor" aria-label="Permalink: Change Log" href="#change-log"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<markdown-accessiblity-table><table>
<thead>
<tr>
<th>Date</th>
<th>Responsible Party</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>2024-09-01</td>
<td>@lornajane</td>
<td>Initial draft</td>
</tr>
</tbody>
</table></markdown-accessiblity-table>
<div class="markdown-heading" dir="auto"><h2 tabindex="-1" class="heading-element" dir="auto">Introduction</h2><a id="user-content-introduction" class="anchor" aria-label="Permalink: Introduction" href="#introduction"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<p dir="auto">Evolve the existing <code>tags</code> implementation to (optionally) support more use cases, such as giving the tags some grouping/relationships and adding more metadata.</p>
<div class="markdown-heading" dir="auto"><h2 tabindex="-1" class="heading-element" dir="auto">Motivation</h2><a id="user-content-motivation" class="anchor" aria-label="Permalink: Motivation" href="#motivation"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<p dir="auto">The tags feature hasn't changed since the spec was still called Swagger, but it's one of the most-extended aspects of OpenAPI with most tools supporting some sort of grouping or additional metadata. One motivation for this proposal is to "pave the cowpath" and formalise some of the patterns from those extensions as part of the specification.</p>
<p dir="auto">The existing tags implementation is also quite limiting, so users/tools feel they "cannot" use tags, because they are so widely implemented for documentation navigation and required exactly one tag per operation, to be used only for this single purpose or to be opted out using extensions such as <code>x-traitTag</code>. The result is that we see lots of extensions that add arbitrary metadata to operations, some of them even become part of the specification officially (looking at you, <code>deprecated: true</code>) or being so widely used that we should probably adopt them (<code>x-internal</code>, <code>x-experimental</code>). The specification does have a way of tagging operations, but it's too limited and the result is that everything has to be added as an extension field.</p>
<p dir="auto">On a personal note, I work for a tool vendor and was proposing these changes internally; but the problems affect all OpenAPI users so I brought it to the main project.</p>
<div class="markdown-heading" dir="auto"><h3 tabindex="-1" class="heading-element" dir="auto">Supporting evidence</h3><a id="user-content-supporting-evidence" class="anchor" aria-label="Permalink: Supporting evidence" href="#supporting-evidence"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<p dir="auto">There are several examples "in the wild" of where a better tags implementation would have helped. Here is a selection of publicly-accessible examples to illustrate some of the problems this proposal could help with:</p>
<ul dir="auto">
<li>Grouping of tags is a very common use case, almost everyone uses some sort of extra hierarchy to group the tags themselves, which makes sense as our APIs are only getting more complex, something like <a href="https://redocly.com/docs/api-reference-docs/specification-extensions/x-tag-groups/" rel="nofollow"><code>x-tagGroups</code></a> is a good example - and there's a <a href="https://github.com/OAI/OpenAPI-Specification/issues/1367" data-hovercard-type="issue" data-hovercard-url="/OAI/OpenAPI-Specification/issues/1367/hovercard">very active open issue on OpenAPI specification itself</a></li>
<li>Various tag-alike additions exist, sometimes called "badges" or similar; I'd include extensions such as <a href="https://redocly.com/docs/cli/guides/hide-apis/#step-1-add-x-internal-to-the-api-description" rel="nofollow"><code>x-internal</code></a> as a tag-alike since they could be tags if more than one tag (or tag type) could be applied.</li>
<li>Additional display metadata is also in active use in the wild, see <a href="https://redocly.com/docs/api-reference-docs/specification-extensions/x-display-name" rel="nofollow"><code>x-displayName</code></a> and this <a href="https://github.com/OAI/OpenAPI-Specification/issues/2843" data-hovercard-type="issue" data-hovercard-url="/OAI/OpenAPI-Specification/issues/2843/hovercard">OpenAPI specification issue</a></li>
</ul>
<div class="markdown-heading" dir="auto"><h2 tabindex="-1" class="heading-element" dir="auto">Proposed solution</h2><a id="user-content-proposed-solution" class="anchor" aria-label="Permalink: Proposed solution" href="#proposed-solution"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<p dir="auto">Originally proposed in a <a href="https://github.com/OAI/sig-moonwalk/discussions/67" data-hovercard-type="discussion" data-hovercard-url="/OAI/sig-moonwalk/discussions/67/hovercard">Moonwalk discussion</a>, I am proposing three backwards-compatible additions to the existing tags feature:</p>
<ul dir="auto">
<li>Tags get a <code>summary</code> alongside <code>name</code> and <code>description</code>. In keeping with our existing practices: name is the identifier, summary is the short display content, and description is available in contexts where more information is appropriate.</li>
<li>A <code>parent</code> field is added to support a hierarchy without adding either separators or a new data type. Your tag can belong to another tag.</li>
<li>A <code>kind</code> field to explain which family of tags this tag belongs to (previously proposed as <code>type</code>). We'd expecting these to be <code>nav</code>, <code>badge</code>, <code>internal</code> and probably some other things that other tooling types would find useful.</li>
</ul>
<p dir="auto">An example could look something like this:</p>
<div class="highlight highlight-source-yaml notranslate position-relative overflow-auto" dir="auto" data-snippet-clipboard-copy-content="tags:
- name: deprecated
  kind: internal
  summary: Deprecated
  description: This operation has been deprecated and will be removed in the future. Avoid using items with this tag.
- name: shop
  kind: nav
  summary: Order Online
  description: Operations relating to the retail operations behind the [online shopping site](https://example.com/shopping).
- name: products
  kind: nav
  parent: shop
  summary: Products
  description: View and manage the product catalog.
- name: orders
  kind: nav
  parent: shop
  summary: Online Orders
  description: Place, fulfil and invoice orders for the online shop.
"><pre><span class="pl-ent">tags</span>:
- <span class="pl-ent">name</span>: <span class="pl-s">deprecated</span>
  <span class="pl-ent">kind</span>: <span class="pl-s">internal</span>
  <span class="pl-ent">summary</span>: <span class="pl-s">Deprecated</span>
  <span class="pl-ent">description</span>: <span class="pl-s">This operation has been deprecated and will be removed in the future. Avoid using items with this tag.</span>
- <span class="pl-ent">name</span>: <span class="pl-s">shop</span>
  <span class="pl-ent">kind</span>: <span class="pl-s">nav</span>
  <span class="pl-ent">summary</span>: <span class="pl-s">Order Online</span>
  <span class="pl-ent">description</span>: <span class="pl-s">Operations relating to the retail operations behind the [online shopping site](https://example.com/shopping).</span>
- <span class="pl-ent">name</span>: <span class="pl-s">products</span>
  <span class="pl-ent">kind</span>: <span class="pl-s">nav</span>
  <span class="pl-ent">parent</span>: <span class="pl-s">shop</span>
  <span class="pl-ent">summary</span>: <span class="pl-s">Products</span>
  <span class="pl-ent">description</span>: <span class="pl-s">View and manage the product catalog.</span>
- <span class="pl-ent">name</span>: <span class="pl-s">orders</span>
  <span class="pl-ent">kind</span>: <span class="pl-s">nav</span>
  <span class="pl-ent">parent</span>: <span class="pl-s">shop</span>
  <span class="pl-ent">summary</span>: <span class="pl-s">Online Orders</span>
  <span class="pl-ent">description</span>: <span class="pl-s">Place, fulfil and invoice orders for the online shop.</span>
</pre></div>
<p dir="auto">Rather than making an allowed list of kinds, we will instead leave that open for user extension and keep a list of the recommended/expected types in a registry and evolve that as conventions emerge.</p>
<div class="markdown-heading" dir="auto"><h2 tabindex="-1" class="heading-element" dir="auto">Detailed design</h2><a id="user-content-detailed-design" class="anchor" aria-label="Permalink: Detailed design" href="#detailed-design"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<p dir="auto">The following section is an updated specification section, for the top-level tags object only (no other changes are needed):</p>
<hr>
<div class="markdown-heading" dir="auto"><h4 tabindex="-1" class="heading-element" dir="auto">Tag Object</h4><a id="user-content-tag-object" class="anchor" aria-label="Permalink: Tag Object" href="#tag-object"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<p dir="auto">Adds metadata to a single tag that is used by the <a href="#operation-object">Operation Object</a>.
Each tag used in the Operation Object instances MAY have a Tag Object defined.</p>
<div class="markdown-heading" dir="auto"><h5 tabindex="-1" class="heading-element" dir="auto">Fixed Fields</h5><a id="user-content-fixed-fields" class="anchor" aria-label="Permalink: Fixed Fields" href="#fixed-fields"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<markdown-accessiblity-table><table>
<thead>
<tr>
<th>Field Name</th>
<th align="center">Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><a name="user-content-tagname"></a>name</td>
<td align="center"><code>string</code></td>
<td><strong>REQUIRED</strong>. The name of the tag. Use this value in the <code>tags</code> array of an Operation.</td>
</tr>
<tr>
<td><a name="user-content-tagsummary"></a>summary</td>
<td align="center"><code>string</code></td>
<td>A short summary of the tag, used for display purposes.</td>
</tr>
<tr>
<td><a name="user-content-tagdescription"></a>description</td>
<td align="center"><code>string</code></td>
<td>A description for the tag. <a href="https://spec.commonmark.org/" rel="nofollow">CommonMark syntax</a> MAY be used for rich text representation.</td>
</tr>
<tr>
<td><a name="user-content-tagexternaldocs"></a>externalDocs</td>
<td align="center"><a href="#external-documentation-object">External Documentation Object</a></td>
<td>Additional external documentation for this tag.</td>
</tr>
<tr>
<td><a name="user-content-tagparent"></a>parent</td>
<td align="center"><code>string</code></td>
<td>The <code>name</code> of a tag that this tags is nested under. The named tag MUST exist in the API description, and circular references between parent and child tags MUST NOT be used.</td>
</tr>
<tr>
<td><a name="user-content-tagkind"></a>kind</td>
<td align="center"><code>string</code></td>
<td>A machine-readable string to categorize what sort of tag it is. Common uses are <code>nav</code> for Navigation, <code>badge</code> for badges, <code>internal</code> for internal APIs, but any string value can be used. A registry of known values is available.</td>
</tr>
</tbody>
</table></markdown-accessiblity-table>
<p dir="auto">This object MAY be extended with <a href="#specification-extensions">Specification Extensions</a>.</p>
<div class="markdown-heading" dir="auto"><h5 tabindex="-1" class="heading-element" dir="auto">Tag Object Example</h5><a id="user-content-tag-object-example" class="anchor" aria-label="Permalink: Tag Object Example" href="#tag-object-example"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<div class="highlight highlight-source-json notranslate position-relative overflow-auto" dir="auto" data-snippet-clipboard-copy-content="{
  &quot;name&quot;: &quot;account-updates&quot;,
  &quot;summary&quot;: &quot;Account Updates&quot;,
  &quot;description&quot;: &quot;Account update operations&quot;,
  &quot;kind&quot;: &quot;nav&quot;
},
{
  &quot;name&quot;: &quot;partner&quot;,
  &quot;summary&quot;: &quot;Partner&quot;,
  &quot;description&quot;: &quot;Operations available to the partners network&quot;,
  &quot;parent&quot;: &quot;external&quot;,
  &quot;kind&quot;: &quot;audience&quot;
},
{
  &quot;name&quot;: &quot;external&quot;,
  &quot;summary&quot;: &quot;External&quot;,
  &quot;description&quot;: &quot;Operations available to external consumers&quot;,
  &quot;kind&quot;: &quot;audience&quot;
}"><pre>{
  <span class="pl-ent">"name"</span>: <span class="pl-s"><span class="pl-pds">"</span>account-updates<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"summary"</span>: <span class="pl-s"><span class="pl-pds">"</span>Account Updates<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"description"</span>: <span class="pl-s"><span class="pl-pds">"</span>Account update operations<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"kind"</span>: <span class="pl-s"><span class="pl-pds">"</span>nav<span class="pl-pds">"</span></span>
},
{
  <span class="pl-ent">"name"</span>: <span class="pl-s"><span class="pl-pds">"</span>partner<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"summary"</span>: <span class="pl-s"><span class="pl-pds">"</span>Partner<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"description"</span>: <span class="pl-s"><span class="pl-pds">"</span>Operations available to the partners network<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"parent"</span>: <span class="pl-s"><span class="pl-pds">"</span>external<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"kind"</span>: <span class="pl-s"><span class="pl-pds">"</span>audience<span class="pl-pds">"</span></span>
},
{
  <span class="pl-ent">"name"</span>: <span class="pl-s"><span class="pl-pds">"</span>external<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"summary"</span>: <span class="pl-s"><span class="pl-pds">"</span>External<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"description"</span>: <span class="pl-s"><span class="pl-pds">"</span>Operations available to external consumers<span class="pl-pds">"</span></span>,
  <span class="pl-ent">"kind"</span>: <span class="pl-s"><span class="pl-pds">"</span>audience<span class="pl-pds">"</span></span>
}</pre></div>
<div class="highlight highlight-source-yaml notranslate position-relative overflow-auto" dir="auto" data-snippet-clipboard-copy-content="- name: account-updates
  summary: Account Updates
  description: Account update operations
  kind: nav

- name: partner
  summary: Partner
  description: Operations available to the partners network
  parent: external
  kind: audience

- name: external
  summary: External
  description: Operations available to external consumers
  kind: audience"><pre>- <span class="pl-ent">name</span>: <span class="pl-s">account-updates</span>
  <span class="pl-ent">summary</span>: <span class="pl-s">Account Updates</span>
  <span class="pl-ent">description</span>: <span class="pl-s">Account update operations</span>
  <span class="pl-ent">kind</span>: <span class="pl-s">nav</span>

- <span class="pl-ent">name</span>: <span class="pl-s">partner</span>
  <span class="pl-ent">summary</span>: <span class="pl-s">Partner</span>
  <span class="pl-ent">description</span>: <span class="pl-s">Operations available to the partners network</span>
  <span class="pl-ent">parent</span>: <span class="pl-s">external</span>
  <span class="pl-ent">kind</span>: <span class="pl-s">audience</span>

- <span class="pl-ent">name</span>: <span class="pl-s">external</span>
  <span class="pl-ent">summary</span>: <span class="pl-s">External</span>
  <span class="pl-ent">description</span>: <span class="pl-s">Operations available to external consumers</span>
  <span class="pl-ent">kind</span>: <span class="pl-s">audience</span></pre></div>
<hr>
<div class="markdown-heading" dir="auto"><h2 tabindex="-1" class="heading-element" dir="auto">Backwards compatibility</h2><a id="user-content-backwards-compatibility" class="anchor" aria-label="Permalink: Backwards compatibility" href="#backwards-compatibility"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<p dir="auto">All new fields are optional, so existing API descriptions will remain valid and useful.
Some users may wish to adopt some of the following steps on upgrade:</p>
<ul dir="auto">
<li>Set <code>kind: nav</code> if their existing tags are currently used for navigation entries in documentation tooling.</li>
<li>Change <code>x-displayName</code> in <code>tag</code> objects to <code>summary</code> instead.</li>
<li>Add a tag to replace each <code>x-tagGroups</code> entry, and set the <code>parent</code> field for each of the tags in the groups.</li>
<li>Change <code>x-badges</code> extensions to instead be a tag with <code>kind: badge</code>.</li>
<li>Change features like <code>x-internal</code> to be a tag with a specific <code>kind</code> set. Similarly some lifecycle use cases such as <code>x-beta</code> could be replaced with tags.</li>
</ul>
<div class="markdown-heading" dir="auto"><h2 tabindex="-1" class="heading-element" dir="auto">Alternatives considered</h2><a id="user-content-alternatives-considered" class="anchor" aria-label="Permalink: Alternatives considered" href="#alternatives-considered"><svg data-component="Octicon" class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div>
<ul dir="auto">
<li>
<p dir="auto">Continue to use tags as-is, and extend the spec for each use case that users need rather than providing an open metadata implementation.
We've been slow to iterate and I would rather "open" the options than try to control them.
The API space evolves quite quickly.</p>
</li>
<li>
<p dir="auto">Set <code>children</code> rather than <code>parent</code> on the tags and operate a top-down relationship.
The suggestion of allowing multiple links or a graph approach was also mentioned.
In both cases, there are good ideas in every direction, but our responsibility is to implement a structure that users can easily understand and maintain.</p>
</li>
</ul>
</article></div><div class="d-none"></div></section></div></div></div> </div> <!-- --> </div></div></div></div></div></div><div class="ScrollMarksContainer-module__scrollMarksContainer__Eu7uU" id="find-result-marks-container"></div><div class="d-none"></div><div class="d-none"></div></div> <!-- --> <!-- --> </div>
</react-app>


  </div>

</turbo-frame>

    </main>
  </div>

  </div>

          <footer class="footer tmp-pt-7 tmp-pb-6 f6 color-fg-muted color-border-subtle p-responsive" role="contentinfo" >
  <h2 class='sr-only'>Footer</h2>


  <div class="d-flex flex-justify-center flex-items-center flex-column-reverse flex-lg-row flex-wrap flex-lg-nowrap">
    <div class="d-flex flex-items-center flex-shrink-0 mx-2">
      <a aria-label="GitHub Homepage" class="footer-octicon mr-2" href="https://github.com">
        <svg aria-hidden="true" data-component="Octicon" height="24" viewBox="0 0 24 24" version="1.1" width="24" data-view-component="true" class="octicon octicon-mark-github">
    <path d="M10.226 17.284c-2.965-.36-5.054-2.493-5.054-5.256 0-1.123.404-2.336 1.078-3.144-.292-.741-.247-2.314.09-2.965.898-.112 2.111.36 2.83 1.01.853-.269 1.752-.404 2.853-.404 1.1 0 1.999.135 2.807.382.696-.629 1.932-1.1 2.83-.988.315.606.36 2.179.067 2.942.72.854 1.101 2 1.101 3.167 0 2.763-2.089 4.852-5.098 5.234.763.494 1.28 1.572 1.28 2.807v2.336c0 .674.561 1.056 1.235.786 4.066-1.55 7.255-5.615 7.255-10.646C23.5 6.188 18.334 1 11.978 1 5.62 1 .5 6.188.5 12.545c0 4.986 3.167 9.12 7.435 10.669.606.225 1.19-.18 1.19-.786V20.63a2.9 2.9 0 0 1-1.078.224c-1.483 0-2.359-.808-2.987-2.313-.247-.607-.517-.966-1.034-1.033-.27-.023-.359-.135-.359-.27 0-.27.45-.471.898-.471.652 0 1.213.404 1.797 1.235.45.651.921.943 1.483.943.561 0 .92-.202 1.437-.719.382-.381.674-.718.944-.943"></path>
</svg>
</a>
      <span>
        &copy; 2026 GitHub,&nbsp;Inc.
      </span>
    </div>

    <nav aria-label="Footer">
      <h3 class="sr-only" id="sr-footer-heading">Footer navigation</h3>

      <ul class="list-style-none d-flex flex-justify-center flex-wrap mb-2 mb-lg-0" aria-labelledby="sr-footer-heading">


          <li class="mx-2">
            <a data-analytics-event="{&quot;category&quot;:&quot;Footer&quot;,&quot;action&quot;:&quot;go to Terms&quot;,&quot;label&quot;:&quot;text:terms&quot;}" href="https://docs.github.com/site-policy/github-terms/github-terms-of-service" data-view-component="true" class="Link--secondary Link">Terms</a>
          </li>

          <li class="mx-2">
            <a data-analytics-event="{&quot;category&quot;:&quot;Footer&quot;,&quot;action&quot;:&quot;go to privacy&quot;,&quot;label&quot;:&quot;text:privacy&quot;}" href="https://docs.github.com/site-policy/privacy-policies/github-privacy-statement" data-view-component="true" class="Link--secondary Link">Privacy</a>
          </li>

          <li class="mx-2">
            <a data-analytics-event="{&quot;category&quot;:&quot;Footer&quot;,&quot;action&quot;:&quot;go to security&quot;,&quot;label&quot;:&quot;text:security&quot;}" href="https://github.com/security" data-view-component="true" class="Link--secondary Link">Security</a>
          </li>

          <li class="mx-2">
            <a data-analytics-event="{&quot;category&quot;:&quot;Footer&quot;,&quot;action&quot;:&quot;go to status&quot;,&quot;label&quot;:&quot;text:status&quot;}" href="https://www.githubstatus.com/" data-view-component="true" class="Link--secondary Link">Status</a>
          </li>

          <li class="mx-2">
            <a data-analytics-event="{&quot;category&quot;:&quot;Footer&quot;,&quot;action&quot;:&quot;go to community&quot;,&quot;label&quot;:&quot;text:community&quot;}" href="https://github.community/" data-view-component="true" class="Link--secondary Link">Community</a>
          </li>

          <li class="mx-2">
            <a data-analytics-event="{&quot;category&quot;:&quot;Footer&quot;,&quot;action&quot;:&quot;go to docs&quot;,&quot;label&quot;:&quot;text:docs&quot;}" href="https://docs.github.com/" data-view-component="true" class="Link--secondary Link">Docs</a>
          </li>

          <li class="mx-2">
            <a data-analytics-event="{&quot;category&quot;:&quot;Footer&quot;,&quot;action&quot;:&quot;go to contact&quot;,&quot;label&quot;:&quot;text:contact&quot;}" href="https://support.github.com?tags=dotcom-footer" data-view-component="true" class="Link--secondary Link">Contact</a>
          </li>

          <li class="mx-2" >
  <cookie-consent-link>
    <button
      type="button"
      class="Link--secondary underline-on-hover border-0 p-0 color-bg-transparent"
      data-action="click:cookie-consent-link#showConsentManagement"
      data-analytics-event="{&quot;location&quot;:&quot;footer&quot;,&quot;action&quot;:&quot;cookies&quot;,&quot;context&quot;:&quot;subfooter&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;label&quot;:&quot;cookies_link_subfooter_footer&quot;}"
    >
       Manage cookies
    </button>
  </cookie-consent-link>
</li>

<li class="mx-2">
  <cookie-consent-link>
    <button
      type="button"
      class="Link--secondary underline-on-hover border-0 p-0 color-bg-transparent text-left"
      data-action="click:cookie-consent-link#showConsentManagement"
      data-analytics-event="{&quot;location&quot;:&quot;footer&quot;,&quot;action&quot;:&quot;dont_share_info&quot;,&quot;context&quot;:&quot;subfooter&quot;,&quot;tag&quot;:&quot;link&quot;,&quot;label&quot;:&quot;dont_share_info_link_subfooter_footer&quot;}"
    >
      Do not share my personal information
    </button>
  </cookie-consent-link>
</li>

      </ul>
    </nav>
  </div>
</footer>


    <ghcc-consent id="ghcc" class="position-fixed bottom-0 left-0" style="z-index: 999999"
      data-locale="en"
      data-initial-cookie-consent-allowed=""
      data-cookie-consent-required="false"
    ></ghcc-consent>


  <div id="ajax-error-message" class="ajax-error-message flash flash-error" hidden>
    <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-alert">
    <path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path>
</svg>
    <button type="button" class="flash-close js-ajax-error-dismiss" aria-label="Dismiss error">
      <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-x">
    <path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"></path>
</svg>
    </button>
    You can’t perform that action at this time.
  </div>

    <template id="site-details-dialog">
  <details class="details-reset details-overlay details-overlay-dark lh-default color-fg-default hx_rsm" open>
    <summary role="button" aria-label="Close dialog"></summary>
    <details-dialog class="Box Box--overlay d-flex flex-column anim-fade-in fast hx_rsm-dialog hx_rsm-modal">
      <button class="Box-btn-octicon m-0 btn-octicon position-absolute right-0 top-0" type="button" aria-label="Close dialog" data-close-dialog>
        <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-x">
    <path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"></path>
</svg>
      </button>
      <div class="octocat-spinner tmp-my-6 js-details-dialog-spinner"></div>
    </details-dialog>
  </details>
</template>

    <div class="Popover js-hovercard-content position-absolute" style="display: none; outline: none;">
  <div class="Popover-message Popover-message--bottom-left Popover-message--large Box color-shadow-large" style="width:360px;">
  </div>
</div>

    <template id="snippet-clipboard-copy-button">
  <div class="zeroclipboard-container position-absolute right-0 top-0">
    <clipboard-copy aria-label="Copy code to clipboard" class="ClipboardButton btn js-clipboard-copy m-2 p-0" data-copy-feedback="Copied!" data-tooltip-direction="w">
      <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon m-2 tmp-m-2">
    <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
</svg>
      <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-check js-clipboard-check-icon color-fg-success d-none m-2 tmp-m-2">
    <path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path>
</svg>
    </clipboard-copy>
  </div>
</template>
<template id="snippet-clipboard-copy-button-unpositioned">
  <div class="zeroclipboard-container">
    <clipboard-copy aria-label="Copy code to clipboard" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w">
      <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon">
    <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
</svg>
      <svg aria-hidden="true" data-component="Octicon" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-check js-clipboard-check-icon color-fg-success d-none">
    <path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path>
</svg>
    </clipboard-copy>
  </div>
</template>


    </div>
    <div id="js-global-screen-reader-notice" class="sr-only mt-n1" aria-live="polite" aria-atomic="true" ></div>
    <div id="js-global-screen-reader-notice-assertive" class="sr-only mt-n1" aria-live="assertive" aria-atomic="true"></div>
  </body>
</html>
