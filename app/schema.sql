drop table if exists feedbacks;
create table feedbacks (
  id integer primary key autoincrement,
  textFeedback string not null,
  textInput string not null,
  persModels string not null,
  nonpersModels string not null,
  persuasive string not null,
  wordCount string not null,
  readabilityScore string not null,
  ReadabilityGrade string not null,
  DiractionCount string not null,
  WPS string not null,
  Sixltr string not null,
  pronoun string not null,
  ppron string not null,
  i string not null,
  you string not null,
  ipron string not null,
  prep string not null,
  auxverb string not null,
  negate string not null,
  numbers string not null,
  focuspast string not null,
  focuspresent string not null,
  AllPunc string not null,
  Comma string not null,
  QMark string not null,
  Exemplify string not null
);
