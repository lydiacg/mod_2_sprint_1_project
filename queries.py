question_list = """
SELECT questionid ID, questiontext Question
FROM Question
WHERE questionid IN (1,2,33,115,116)
"""

age_1 = """
WITH ages AS (SELECT a.SurveyID survey_id, a.UserID user_id, a.AnswerText answer,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 18 AND 25 THEN '18-25'
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN '26-35'
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN '36-45'
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN '46-55'
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 65 THEN '56-65'
                WHEN CAST(a.AnswerText AS int) BETWEEN 66 AND 75 THEN '66-75'
                WHEN CAST(a.AnswerText AS int) > 75 THEN 'Over 75' 
                ELSE 'Under 18'
            END AS age_group
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid
            WHERE q.questionid = 1)

SELECT age_group, COUNT(*)
FROM ages
GROUP BY age_group
"""

age_2 = """
WITH ages AS (SELECT a.SurveyID survey_id, a.UserID user_id, a.AnswerText answer,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 18 AND 25 THEN '18-25'
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN '26-35'
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN '36-45'
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN '46-55'
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 65 THEN '56-65'
                WHEN CAST(a.AnswerText AS int) BETWEEN 66 AND 75 THEN '66-75'
                WHEN CAST(a.AnswerText AS int) > 75 THEN 'Over 75' 
                ELSE 'Under 18'
            END AS age_group
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid
            WHERE q.questionid = 1),
    young_worker AS (SELECT age_group, user_id, answer
                        FROM ages
                        WHERE age_group IN ('Under 18')
                        ORDER BY CAST(answer AS int))
    
SELECT 
a.AnswerText, y.answer 
FROM Answer a
JOIN Question q
ON a.QuestionID = q.questionid
JOIN young_worker y
ON a.UserID = y.user_id

WHERE q.questiontext = 'What country do you live in?'
 AND y.answer > 0
ORDER BY CAST(y.answer AS int) DESC
"""

age_3 = """
WITH ages AS (SELECT a.SurveyID survey_id, a.UserID user_id, a.AnswerText answer,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 15 AND 25 THEN 'Under 25'
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN '26-35'
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN '36-45'
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN '46-55'
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 67 THEN 'Over 55'
                ELSE 'Other'
            END AS age_group
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid
            WHERE q.questionid = 1 AND age_group != 'Other') 

SELECT survey_id, age_group, COUNT(*)
FROM ages
GROUP BY 1,2
ORDER BY 1,answer
"""

top_10_countries = """
SELECT 
    CASE 
        WHEN a.AnswerText LIKE '%America%' OR a.AnswerText = 'United States' OR a.AnswerText = 'USA' THEN 'America'
        ELSE a.AnswerText
    END as answer,
    COUNT(*) number
FROM Answer a
JOIN Question q
ON a.QuestionID = q.questionid

WHERE q.questiontext = 'What country do you live in?'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
"""

gender_1 = """
WITH genders AS (SELECT a.SurveyID survey_id, LOWER(a.AnswerText) gender
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 2)

SELECT survey_id, gender, COUNT(*) number
FROM genders
GROUP BY 1,2
ORDER BY 1,3 DESC
"""

gender_2 = """
WITH genders AS (SELECT a.SurveyID survey_id, 
                            CASE
                                WHEN LOWER(a.AnswerText) = 'male' THEN 'male'
                                WHEN LOWER(a.AnswerText) = 'female' THEN 'female'
                                WHEN a.AnswerText IN ('43',  '-1') THEN 'invalid'
                                ELSE 'TGNB'
                            END AS gender
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 2
                        AND gender != 'invalid' )     

SELECT survey_id, gender, COUNT(*) number
FROM genders
GROUP BY 1,2
ORDER BY 1,3 DESC                                      
"""

num_mental_disorders_16_19 = """
WITH responses AS (SELECT a.SurveyID survey_id, 
                        CASE
                            WHEN a.AnswerText = 'No' THEN 'No'
                            WHEN a.AnswerText = 'Yes' THEN 'Yes'
                            WHEN a.AnswerText = "Don't Know" THEN "Don't Know"
                            WHEN a.AnswerText = 'Maybe' OR a.AnswerText = 'Possibly' THEN 'Maybe'
                        END answer
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 33)

SELECT survey_id, answer, COUNT(*)
FROM responses
GROUP BY 1,2
"""

num_mental_disorders_14 = """
WITH responses AS (SELECT a.SurveyID survey_id, 
                        CASE
                            WHEN a.AnswerText = '-1' THEN 'No'
                            ELSE 'Yes'
                        END answer
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 92)

SELECT survey_id, answer, COUNT(*)
FROM responses
GROUP BY 1,2
"""

num_mental_disorders_16_19_agg = """
WITH responses AS (SELECT a.SurveyID survey_id, 
                        CASE
                            WHEN a.AnswerText = 'No' OR a.AnswerText = "Don't Know" THEN 'No'
                            WHEN a.AnswerText = 'Yes' OR a.AnswerText = 'Maybe' OR a.AnswerText = 'Possibly' THEN 'Yes'
                        END answer
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 33)

SELECT survey_id, answer, COUNT(*)
FROM responses
GROUP BY 1,2
"""

num_mental_disorders_16_19_agg_age = """
WITH ages AS (SELECT a.SurveyID survey_id, a.UserID user_id, a.AnswerText answer,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 15 AND 25 THEN 'Under 25'
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN '26-35'
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN '36-45'
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN '46-55'
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 67 THEN 'Over 55'
                ELSE 'Other'
            END AS age_group,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 15 AND 25 THEN 1
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN 2
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN 3
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN 4
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 67 THEN 5
                ELSE 'Other'
            END AS ordering
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid
            WHERE q.questionid = 1 AND age_group != 'Other') ,
    responses AS (SELECT a.SurveyID survey_id, a.UserID user_id,
                        CASE
                            WHEN a.AnswerText = 'No' OR a.AnswerText = "Don't Know" THEN 'No'
                            WHEN a.AnswerText = 'Yes' OR a.AnswerText = 'Maybe' OR a.AnswerText = 'Possibly' THEN 'Yes'
                        END answer
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 33)

SELECT a.survey_id, a.age_group age, r.answer response, COUNT(*)
FROM responses r
JOIN ages a
ON a.survey_id = r.survey_id AND a.user_id = r.user_id
GROUP BY 1,2,3
ORDER BY 1,a.ordering,4
"""

num_mental_disorders_14_age = """
WITH ages AS (SELECT a.SurveyID survey_id, a.UserID user_id, a.AnswerText answer,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 15 AND 25 THEN 'Under 25'
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN '26-35'
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN '36-45'
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN '46-55'
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 67 THEN 'Over 55'
                ELSE 'Other'
            END AS age_group,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 15 AND 25 THEN 1
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN 2
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN 3
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN 4
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 67 THEN 5
                ELSE 'Other'
            END AS ordering
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid
            WHERE q.questionid = 1 AND age_group != 'Other') ,
    responses AS (SELECT a.SurveyID survey_id, a.UserID user_id,
                        CASE
                            WHEN a.AnswerText = '-1' THEN 'No'
                            ELSE 'Yes'
                        END answer
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 92)

SELECT a.survey_id, a.age_group age, r.answer response, COUNT(*)
FROM responses r
JOIN ages a
ON a.survey_id = r.survey_id AND a.user_id = r.user_id
GROUP BY 1,2,3
ORDER BY 1,a.ordering,4
"""

num_mental_disorders_16_19_agg_gender = """
WITH genders AS (SELECT a.SurveyID survey_id, a.UserID user_id, 
                            CASE
                                WHEN LOWER(a.AnswerText) = 'male' THEN 'male'
                                WHEN LOWER(a.AnswerText) = 'female' THEN 'female'
                                WHEN a.AnswerText IN ('43',  '-1') THEN 'invalid'
                                ELSE 'TGNB'
                            END AS gender,
                            CASE
                                WHEN LOWER(a.AnswerText) = 'male' THEN 2
                                WHEN LOWER(a.AnswerText) = 'female' THEN 1
                                WHEN a.AnswerText IN ('43',  '-1') THEN 4
                                ELSE 3
                            END AS ordering
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 2
                        AND gender != 'invalid' ) ,
    responses AS (SELECT a.SurveyID survey_id, a.UserID user_id,
                        CASE
                            WHEN a.AnswerText = 'No' OR a.AnswerText = "Don't Know" THEN 'No'
                            WHEN a.AnswerText = 'Yes' OR a.AnswerText = 'Maybe' OR a.AnswerText = 'Possibly' THEN 'Yes'
                        END answer
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 33)

SELECT g.survey_id, g.gender gender, r.answer response, COUNT(*)
FROM responses r
JOIN genders g
ON g.survey_id = r.survey_id AND g.user_id = r.user_id
GROUP BY 1,2,3
ORDER BY 1,g.ordering,4
"""

num_mental_disorders_14_gender = """
WITH genders AS (SELECT a.SurveyID survey_id, a.UserID user_id,
                            CASE
                                WHEN LOWER(a.AnswerText) = 'male' THEN 'male'
                                WHEN LOWER(a.AnswerText) = 'female' THEN 'female'
                                WHEN a.AnswerText IN ('43',  '-1') THEN 'invalid'
                                ELSE 'TGNB'
                            END AS gender,
                            CASE
                                WHEN LOWER(a.AnswerText) = 'male' THEN 2
                                WHEN LOWER(a.AnswerText) = 'female' THEN 1
                                WHEN a.AnswerText IN ('43',  '-1') THEN 4
                                ELSE 3
                            END AS ordering
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 2
                        AND gender != 'invalid' ) ,
    responses AS (SELECT a.SurveyID survey_id, a.UserID user_id,
                        CASE
                            WHEN a.AnswerText = '-1' THEN 'No'
                            ELSE 'Yes'
                        END answer
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 92)

SELECT g.survey_id, g.gender gender, r.answer response, COUNT(*)
FROM responses r
JOIN genders g
ON g.survey_id = r.survey_id AND g.user_id = r.user_id
GROUP BY 1,2,3
ORDER BY 1,g.ordering,4
"""

top_4_disorders = """
WITH diagnosis AS (SELECT a.SurveyID survey_id, a.UserID user_id,

            CASE
                WHEN a.AnswerText LIKE '%autism%' OR a.AnswerText LIKE '%Autism%' OR a.AnswerText LIKE '%Asperge%' THEN 'Autism Spectrum Disorder'
                WHEN a.AnswerText LIKE '%Mood Disorder%' OR a.AnswerText LIKE '%Depression%' OR a.AnswerText = 'Seasonal Affective Disorder' or a.AnswerText = 'Suicidal Ideation' THEN 'Mood Disorders'
                WHEN a.AnswerText = 'Pervasive Developmental health disorder (Not Otherwise Specified)' OR a.AnswerText = 'PDD-NOS' THEN 'Pervasive Developmental health disorder (Not Otherwise Specified)' 
                WHEN a.AnswerText = 'Post-traumatic Stress Disorder' OR a.AnswerText LIKE '%PTSD%' THEN 'Post-traumatic Stress Disorder'
                WHEN a.AnswerText = 'Addictive Disorder' OR a.AnswerText = 'Substance Use Disorder' OR a.AnswerText = 'Sexual addiction' THEN 'Addictive Disorders'
                WHEN a.AnswerText = 'Psychotic Disorder (Schizophrenia, Schizoaffective, etc)' OR a.AnswerText = 'Schizotypal Personality Disorder' THEN 'Addictive Disorders'
                WHEN a.AnswerText = 'Attention Deficit Hyperactivity Disorder' OR a.AnswerText = 'ADD (w/o Hyperactivity)' OR a.AnswerText LIKE '%ADHD%' THEN 'ADHD'
                WHEN a.AnswerText LIKE '%Burn%' THEN 'Burnout' 
                WHEN a.AnswerText LIKE '%Anxiety%' OR a.AnswerText LIKE '%anxiety %' THEN 'Anxiety Disorders'
                WHEN a.AnswerText = 'Gender Dysphoria' OR a.AnswerText = 'Transgender' OR a.AnswerText = 'Gender Identity Disorder' THEN 'Gender Identity Disorder/Gender Dyshoria'
                WHEN a.AnswerText LIKE '%epersonal%' THEN 'Depersonalization disorder'
                ELSE a.AnswerText
            END AS diagnosis
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid

            WHERE q.questiontext IN ('If yes, what condition(s) have you been diagnosed with?','If maybe, what condition(s) do you believe you have?')
                AND a.AnswerText != '-1' AND a.AnswerText != "We're all hurt, right?!" AND a.AnswerText != 'Tinnitus')

SELECT
survey_id, diagnosis, COUNT(*)
FROM diagnosis
GROUP BY 1,2
ORDER BY 3 DESC
LIMIT 4
"""

top_4_disorders_age = """
WITH diagnosis AS (SELECT a.SurveyID survey_id, a.UserID user_id,
            CASE
                WHEN a.AnswerText LIKE '%autism%' OR a.AnswerText LIKE '%Autism%' OR a.AnswerText LIKE '%Asperge%' THEN 'Autism/Aspergers'
                WHEN a.AnswerText LIKE '%Mood Disorder%' OR a.AnswerText LIKE '%Depression%' OR a.AnswerText = 'Seasonal Affective Disorder' or a.AnswerText = 'Suicidal Ideation' THEN 'Mood Disorders'
                WHEN a.AnswerText = 'Pervasive Developmental health disorder (Not Otherwise Specified)' OR a.AnswerText = 'PDD-NOS' THEN 'Pervasive Developmental health disorder (Not Otherwise Specified)' 
                WHEN a.AnswerText = 'Post-traumatic Stress Disorder' OR a.AnswerText LIKE '%PTSD%' THEN 'Post-traumatic Stress Disorder'
                WHEN a.AnswerText = 'Addictive Disorder' OR a.AnswerText = 'Substance Use Disorder' OR a.AnswerText = 'Sexual addiction' THEN 'Addictive Disorders'
                WHEN a.AnswerText = 'Psychotic Disorder (Schizophrenia, Schizoaffective, etc)' OR a.AnswerText = 'Schizotypal Personality Disorder' THEN 'Addictive Disorders'
                WHEN a.AnswerText = 'Attention Deficit Hyperactivity Disorder' OR a.AnswerText = 'ADD (w/o Hyperactivity)' OR a.AnswerText LIKE '%ADHD%' THEN 'ADHD'
                WHEN a.AnswerText LIKE '%Burn%' THEN 'Burnout' 
                WHEN a.AnswerText LIKE '%Anxiety%' OR a.AnswerText LIKE '%anxiety %' THEN 'Anxiety Disorders'
                WHEN a.AnswerText = 'Gender Dysphoria' OR a.AnswerText = 'Transgender' OR a.AnswerText = 'Gender Identity Disorder' THEN 'Gender Identity Disorder/Gender Dyshoria'
                WHEN a.AnswerText LIKE '%epersonal%' THEN 'Depersonalization disorder'
                ELSE a.AnswerText
            END AS diagnosis
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid

            WHERE q.questiontext IN ('If yes, what condition(s) have you been diagnosed with?','If maybe, what condition(s) do you believe you have?')
                AND a.AnswerText != '-1' AND a.AnswerText != "We're all hurt, right?!" AND a.AnswerText != 'Tinnitus'),
    counts AS (SELECT
            survey_id, diagnosis, COUNT(*) number
            FROM diagnosis
            GROUP BY 1,2
            ORDER BY 3 DESC
            LIMIT 4),
    ages AS (SELECT a.SurveyID survey_id, a.UserID user_id, a.AnswerText answer,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 15 AND 25 THEN 'Under 25'
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN '26-35'
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN '36-45'
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN '46-55'
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 67 THEN 'Over 55'
                ELSE 'Other'
            END AS age_group,
            CASE 
                WHEN CAST(a.AnswerText AS int) BETWEEN 15 AND 25 THEN 1
                WHEN CAST(a.AnswerText AS int) BETWEEN 26 AND 35 THEN 2
                WHEN CAST(a.AnswerText AS int) BETWEEN 36 AND 45 THEN 3
                WHEN CAST(a.AnswerText AS int) BETWEEN 46 AND 55 THEN 4
                WHEN CAST(a.AnswerText AS int) BETWEEN 56 AND 67 THEN 5
                ELSE 'Other'
            END AS ordering
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid
            WHERE q.questionid = 1 AND age_group != 'Other')                

SELECT d.survey_id, d.diagnosis, a.age_group, COUNT(*)
FROM diagnosis d
JOIN ages a
ON a.survey_id = d.survey_id AND a.user_id = d.user_id
JOIN counts c
ON c.survey_id = d.survey_id AND c.diagnosis = d.diagnosis
GROUP BY 1,2,3
ORDER BY a.ordering, c.number DESC, 4 DESC
"""

top_4_disorders_gender = """
WITH diagnosis AS (SELECT a.SurveyID survey_id, a.UserID user_id,
            CASE
                WHEN a.AnswerText LIKE '%autism%' OR a.AnswerText LIKE '%Autism%' OR a.AnswerText LIKE '%Asperge%' THEN 'Autism/Aspergers'
                WHEN a.AnswerText LIKE '%Mood Disorder%' OR a.AnswerText LIKE '%Depression%' OR a.AnswerText = 'Seasonal Affective Disorder' or a.AnswerText = 'Suicidal Ideation' THEN 'Mood Disorders'
                WHEN a.AnswerText = 'Pervasive Developmental health disorder (Not Otherwise Specified)' OR a.AnswerText = 'PDD-NOS' THEN 'Pervasive Developmental health disorder (Not Otherwise Specified)' 
                WHEN a.AnswerText = 'Post-traumatic Stress Disorder' OR a.AnswerText LIKE '%PTSD%' THEN 'Post-traumatic Stress Disorder'
                WHEN a.AnswerText = 'Addictive Disorder' OR a.AnswerText = 'Substance Use Disorder' OR a.AnswerText = 'Sexual addiction' THEN 'Addictive Disorders'
                WHEN a.AnswerText = 'Psychotic Disorder (Schizophrenia, Schizoaffective, etc)' OR a.AnswerText = 'Schizotypal Personality Disorder' THEN 'Addictive Disorders'
                WHEN a.AnswerText = 'Attention Deficit Hyperactivity Disorder' OR a.AnswerText = 'ADD (w/o Hyperactivity)' OR a.AnswerText LIKE '%ADHD%' THEN 'ADHD'
                WHEN a.AnswerText LIKE '%Burn%' THEN 'Burnout' 
                WHEN a.AnswerText LIKE '%Anxiety%' OR a.AnswerText LIKE '%anxiety %' THEN 'Anxiety Disorders'
                WHEN a.AnswerText = 'Gender Dysphoria' OR a.AnswerText = 'Transgender' OR a.AnswerText = 'Gender Identity Disorder' THEN 'Gender Identity Disorder/Gender Dyshoria'
                WHEN a.AnswerText LIKE '%epersonal%' THEN 'Depersonalization disorder'
                ELSE a.AnswerText
            END AS diagnosis
            FROM Answer a
            JOIN Question q
            ON a.QuestionID = q.questionid

            WHERE q.questiontext IN ('If yes, what condition(s) have you been diagnosed with?','If maybe, what condition(s) do you believe you have?')
                AND a.AnswerText != '-1' AND a.AnswerText != "We're all hurt, right?!" AND a.AnswerText != 'Tinnitus'),
    counts AS (SELECT
            survey_id, diagnosis, COUNT(*) number
            FROM diagnosis
            GROUP BY 1,2
            ORDER BY 3 DESC
            LIMIT 4),
    genders AS (SELECT a.SurveyID survey_id, a.UserID user_id,
                            CASE
                                WHEN LOWER(a.AnswerText) = 'male' THEN 'male'
                                WHEN LOWER(a.AnswerText) = 'female' THEN 'female'
                                WHEN a.AnswerText IN ('43',  '-1') THEN 'invalid'
                                ELSE 'TGNB'
                            END AS gender,
                            CASE
                                WHEN LOWER(a.AnswerText) = 'male' THEN 2
                                WHEN LOWER(a.AnswerText) = 'female' THEN 1
                                WHEN a.AnswerText IN ('43',  '-1') THEN 4
                                ELSE 3
                            END AS ordering
                    FROM Answer a
                    JOIN Question q
                    ON a.QuestionID = q.questionid
                    WHERE q.questionid = 2
                        AND gender != 'invalid' )             

SELECT d.survey_id, d.diagnosis, g.gender, COUNT(*)
FROM diagnosis d
JOIN genders g
ON g.survey_id = d.survey_id AND g.user_id = d.user_id
JOIN counts c
ON c.survey_id = d.survey_id AND c.diagnosis = d.diagnosis
GROUP BY 1,2,3
ORDER BY g.ordering, c.number DESC, 4 DESC
"""