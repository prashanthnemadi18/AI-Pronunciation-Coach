// Common words for game mode practice
export const GAME_WORDS = [
  'hello',
  'world',
  'computer',
  'phone',
  'water',
  'coffee',
  'music',
  'friend',
  'family',
  'house',
  'school',
  'teacher',
  'student',
  'book',
  'paper',
  'pencil',
  'table',
  'chair',
  'window',
  'door',
  'garden',
  'flower',
  'tree',
  'bird',
  'cat',
  'dog',
  'fish',
  'apple',
  'banana',
  'orange',
  'bread',
  'cheese',
  'pizza',
  'chicken',
  'rice',
  'morning',
  'evening',
  'night',
  'today',
  'tomorrow',
  'yesterday',
  'happy',
  'smile',
  'laugh',
  'beautiful',
  'wonderful',
  'amazing',
  'excellent',
  'perfect',
  'great',
];

export const getRandomWord = (): string => {
  const randomIndex = Math.floor(Math.random() * GAME_WORDS.length);
  return GAME_WORDS[randomIndex];
};

export const getRandomWords = (count: number): string[] => {
  const shuffled = [...GAME_WORDS].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
};
