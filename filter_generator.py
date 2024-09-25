from ai_providers import get_ai_result

def filter_for_notion(question):
    request = '''
    You are an expert at converting questions into notion api filters. 
    You will be given a question and you need to return a json that notion can understand. Always include archive as false and 
    remember that the year is 2024
    Here are examples:
    question: All the notes that are created after 2024-09-14 with tag the_content and status done.
    answer: '{
    "filter": {
      "and": [
        {
          "property": "Created",
          "date": {
            "after": "2024-09-10T00:00:00.000Z"
          }
        },
        {
          "property": "Archieve",
          "checkbox": {
            "equals": false
          }
        },
        {
          "property": "Tags",
          "multi_select": {
            "contains": "the_content"
          }
        },
        {
          "property": "statuss",
          "status": {
            "equals": "Done"
          }
        }
      ]
    }
  }'
    question: How many notes have been created after 2024-09-10 that has priority high?
    answer: 
{
    "filter": {
      "and": [
        {
          "property": "Created",
          "date": {
            "after": "2024-09-10T00:00:00.000Z"
          }
        },
        {
          "property": "Archieve",
          "checkbox": {
            "equals": false
          }
        },
        {
          "property": "Priority",
          "select": {
            "equals": "high"
          }
        }
      ]
    }
  }

  List of tags in case i misspelled them:
  anna
    the_content
    ba
    ls
    gat
    notion
    frāzes
    lāpsta
    socializing
    Lauris
    neizdomāta
    nākamie mērķi
    trks
    reminders
    tmtc
    bussiness
    meitenes
    holy grail
    fail
    lente
    3diena
    1diena
    5diena
    data
    hg
    7diena
    6diena
habit
nopirkt
    '''
    return get_ai_result("gpt-4o", request, question, 1000)