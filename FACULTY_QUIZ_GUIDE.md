# Faculty Guide - Creating Quizzes

## How to Create a Module with Quiz

1. **Login as Faculty/Admin**
   - Navigate to "Manage Content" from the navbar

2. **Go to Modules Tab**
   - Click on the "Modules" tab
   - Click "Add New" button

3. **Fill in Module Details**
   - **Title**: Give your module a clear, descriptive title (e.g., "Earthquake Safety Basics")
   - **Description**: Brief summary that students will see (1-2 sentences)
   - **Content**: Detailed educational content about the topic
   - **Image URL**: Optional image to make the module more engaging
   - **Points**: Total points students can earn (e.g., 100, 150, 200)

4. **Create Quiz Questions**

The quiz questions must be in **JSON format**. Here's the correct structure:

```json
[
  {
    "question": "What is the first thing you should do during an earthquake?",
    "options": [
      "Run outside immediately",
      "Drop, Cover, and Hold On",
      "Stand in a doorway",
      "Use the elevator"
    ],
    "correctIndex": 1
  },
  {
    "question": "Which emergency number is for ambulance in India?",
    "options": ["100", "101", "102", "108"],
    "correctIndex": 2
  }
]
```

### Important Rules:

✅ **DO:**
- Use square brackets `[]` to wrap all questions
- Each question is wrapped in curly braces `{}`
- Use double quotes `""` for text
- `correctIndex` starts from 0 (first option = 0, second = 1, etc.)
- Separate questions with commas
- Include at least 5-15 questions for a good quiz

❌ **DON'T:**
- Use single quotes `''`
- Forget commas between questions
- Mix up the correctIndex (remember it starts at 0!)
- Leave trailing commas after the last question

### Quiz JSON Template:

```json
[
  {
    "question": "Your question here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctIndex": 0
  },
  {
    "question": "Another question?",
    "options": ["Choice 1", "Choice 2", "Choice 3"],
    "correctIndex": 1
  },
  {
    "question": "Third question?",
    "options": ["Answer A", "Answer B"],
    "correctIndex": 0
  }
]
```

## How Students Take Quizzes

1. Student logs in and goes to "Modules"
2. Clicks "Take Quiz" on your module
3. Reads the content
4. Answers all quiz questions
5. Clicks "Submit Quiz"
6. Gets instant results:
   - Score percentage
   - Number correct / total
   - Points earned
7. Progress is automatically saved to their profile

## Scoring System

- Students earn points proportional to their score
- Example: If module is worth 150 points and student scores 80%, they earn 120 points
- Score is also saved to their Progress page
- Students can track their achievements and compare on leaderboards

## Tips for Good Quizzes

✅ **Best Practices:**
- Create 10-15 questions per module
- Mix difficulty levels (easy, medium, hard)
- Make questions clear and unambiguous
- Ensure only ONE correct answer per question
- Test your quiz before publishing
- Use real-world scenarios
- Include questions about emergency procedures
- Reference specific numbers (e.g., emergency phone numbers)

## Example Topics for Disaster Preparedness

1. **Earthquake Safety**
   - Richter scale
   - Drop, Cover, Hold On
   - Emergency kit contents
   - Safe locations

2. **Flood Preparedness**
   - Warning signs
   - Evacuation procedures
   - Water safety
   - Emergency supplies

3. **Fire Safety**
   - Prevention methods
   - Escape plans
   - Fire extinguisher use
   - Emergency contacts

4. **Cyclone/Hurricane**
   - Warning systems
   - Shelter preparation
   - Safety during cyclone
   - Post-cyclone safety

5. **First Aid Basics**
   - CPR steps
   - Treating wounds
   - Shock treatment
   - Emergency response

## Validating Your JSON

Before submitting, you can validate your JSON:
1. Copy your quiz JSON
2. Visit: https://jsonlint.com
3. Paste and click "Validate JSON"
4. Fix any errors shown
5. Copy the validated JSON back to the form

## Common JSON Errors

❌ **Error**: `Unexpected token`
- **Fix**: Check for missing commas or quotes

❌ **Error**: `Expected property name`
- **Fix**: Make sure all property names are in double quotes

❌ **Error**: `Trailing comma`
- **Fix**: Remove comma after last item in array/object

## Need Help?

If you encounter any issues:
1. Double-check your JSON format
2. Ensure correctIndex matches your intended answer (remember: 0-based!)
3. Verify all brackets and quotes are matched
4. Test with a simple 2-question quiz first
5. Contact admin if problems persist

---

**Remember**: Quality quizzes help students learn and prepare for real disasters. Make them educational and practical!
