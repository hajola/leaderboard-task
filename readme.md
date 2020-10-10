# Speakly Leaderboard Task

## Some notes

### How to tackle a draw?

As I was tasked of creating a leaderboard function with a return type `List[int]`,
showing a draw, where two users are on the same ranking in the leaderboard is essentially impossible. My initial thinking was guided by the thought to minimize the amount of draws as much as possible.
I had the following ideas to solve draws:
1) Based on number of 'correct_answer' events, and if that ends in a draw, compare the number of 'incorrect_answer' events.
     * As a slow language learner myself it feels to me that grit and persistence should perhaps be awarded equally to getting things right.
2) The sum of all 'correct_answer's and 'incorrect_answer's. 
   * This sounds promising. It would incentivize users to engage with the platform as much as possible. However, going to Speakly website, I saw the word **fastest**. And this got me thinking from two new perspectives.
     * 1) Fastest might also mean, **less time spent**. Later I saw that Speakly advertises "42% of the most important words in 10 hours". So the product values, and wishes to use user's time with maximum learning productivity in mind.
     * 2) Sometimes it is better to just step away from trying to shove something down, and come back to it the next day. Additionally if **any** actvity might help in the leaderboard, it might set a bad precedent and make users annoyed.
3) A ratio of 'correct_answer' and 'incorrect_answer'.
   *  Users shouldnt be afraid of giving wrong answers, and losing a place in the ranking.
4) Random
   * It might seem unfair.

In the end I went with random. Depending on the importance of the leaderboard and other factors, I would potentially revisit the problem.

#### No words learnt, but active?

Some users might have learned no new words, but perhaps had passed the enagegement limit. In that case I include the users in the leaderboard with their score being 0.


## Looking at the completed code block in its entirety - which limitations or possible issues do you see in the code?

Essentially the method I present just transforms data. It is a pipeline with 4 steps. So it's flexibility is very limited. In order to add another constraint  or feature to the leaderboard, code needs to be changed. 

Flexibility could be improved if we sacrificed decoupling. For example, a `lambda` could be passed to `filter_expired_events`. It would increase the flexibility of that pipeline step.

Additionally I see some potential issues with the configparser. Current solution is to have it in a separate class and access it via a static method. For one, using static methods is not very pythonic. In a real world application, the config might come from a database or once in `main` and then shared as needed.

Although type hinting is used in this project, I don't check for types, as this is not user-facing. That might be considered a lack of defensive programming and a possible issue. 

Performance. I have not done performance testing for the algorithm. There is some duplication in terms of filtering/aggregating, which could be optimized. Another approach would be to aggregate all the events right away and then filter. I thought that approach to come with a higher entropy cost. I try to avoid premature optimization.

In the `Event` object that was given, I personally would name them: `event_date` => `date` & `action_name` => `action`. Additionally I would use `enum`s for `action_name` instead.

### Looking at the completed code block in its entirety - are there any patterns or anti-patterns present? If there are,identify them and explain why they are good or bad.

In `tests.py` there are functions `make_event` and `make_multiple_events`. Those functions are only used for testing. However, I have also tested those functions, keeping in mind that the `Event` class might get more complex in the future. This can be considered an anti-pattern, however I can't remember or find what it was called.
