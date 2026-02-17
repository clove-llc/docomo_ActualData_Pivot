CREATE OR REPLACE TABLE `digital-well-456700-i9.docomo_eventActual.facility_special_event_planning_summary` AS

WITH stats_summary AS (
    SELECT
        f_d_a.facility_name,
        -- 施設ごとの直近実績（日付が最大の実績を抽出）
        MAX_BY(f_d_a.actual, f_d_a.date) AS latest_actual
    FROM `digital-well-456700-i9.docomo_eventActual.facility_daily_actual` AS f_d_a
    GROUP BY
        f_d_a.facility_name
)
SELECT
    e_d_b.facility_name AS `施設名`,
    e_d_b.po_level AS `POレベル`,
    e_d_b.branch_office AS `支社`,
    e_d_b.event_type AS `日付種別`,
    ROUND(AVG(f_e_d_m_a.max_actual)) AS `日付実績`,
    ROUND(AVG(s_s.latest_actual)) AS `直近実績`,
    ROUND(AVG(e_d_b.decile_rank)) AS `デシル区分`,
    ROUND(AVG(e_d_b.p25)) AS `25%`, -- 実績下位25%の実績値
    ROUND(AVG(e_d_b.p50)) AS `50%`, -- デシル区分の中央値
    ROUND(AVG(e_d_b.p60)) AS `60%`, -- 実績上位40%の実績値
    ROUND(AVG(e_d_b.p70)) AS `70%`, -- 実績上位30%の実績値
    ROUND(AVG(e_d_b.p75)) AS `75%`, -- 実績上位25%の実績値
    ROUND(AVG(e_d_b.p90)) AS `90%`, -- 実績上位10%の実績値
    ROUND(AVG(e_d_b.max_performance)) AS `MAX`, -- デシル区分の最大の実績値
FROM `digital-well-456700-i9.docomo_eventActual.event_decile_benchmark` AS e_d_b
LEFT JOIN `digital-well-456700-i9.docomo_eventActual.facility_event_decile_max_actual` AS f_e_d_m_a
    ON e_d_b.facility_name = f_e_d_m_a.facility_name
    AND e_d_b.month = f_e_d_m_a.month
    AND e_d_b.week_number_monthly = f_e_d_m_a.week_number_monthly
    AND e_d_b.event_type = f_e_d_m_a.event_type
    AND e_d_b.decile_rank = f_e_d_m_a.decile_rank
LEFT JOIN stats_summary AS s_s
    ON e_d_b.facility_name = s_s.facility_name
WHERE e_d_b.event_type IN ('正月', '年末', 'GW', 'お盆', 'ブラックフライデー')
GROUP BY
    e_d_b.facility_name,
    e_d_b.po_level,
    e_d_b.branch_office,
    e_d_b.event_type
