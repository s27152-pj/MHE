
# Knapsack Problem

Jest to klasyczny problem optymalizacyjny z teorii kombinatoryki.
Polega na tym że:

* Mamy zadany zbiór **N** przedmiotów, gdzie każdy ma przypisaną   
    * wartość **V**
    * wagę **W**
* Mamy plecak o ograniczonej pojemności **C**

* Celem programu jest wybrać takie przedmioty aby:
    * łączna wartość przedmiotów w plecaku była jak największa
    * łączna waga nie przekroczyła pojemności plecaka

## Wybór implementacji

Każdy przedmiot można włożyć do plecaka **(1)**, albo nie **(0)**. Więc nie ma stanów pośrednich

## Struktura projektu
```
├── data/
│ └── input.txt
├── full_enumeration.py
├── genetic_algorithm.py
├── hill_climbing.py
├── knapsack_problem.py
├── README.md # Ten plik
├── run_all.py
├── simulated_annealing.py
└── tabu_search.py
```

## Uruchamianie

Projekt wywołujemy za pomocą linii komend

```
python run_all.py data/input.txt 
```
Oraz dodajemy wartości
* ```--algorithm enum/hcd/hcr/tabu/sa/ga/compare``` - wybieramy jaki algorytm zostanie uruchomiony
* ```--max_iteration (liczba)``` - określamy maksymalną liczbę iteracji
* ```--tabu_size (liczba)``` - określamy maksymalną liczbę tablicy tabu, **Alg. tabu**
* ```--allow_backtrack 0/1``` - wybieramy czy pozwalamy na cofanie się, **Alg. tabu** 
* ```--cooling_schedule exponential/linear``` - wybieramy typ chłodzenia, **Alg. sa**
* ```--alpha (liczba)``` - wybieramy wartość mnożnika szybkości schładzania, **Alg. sa**
* ```--population_size (liczba)``` - wybieramy wielkość populacji, **Alg. ga**
* ```--max_generations (liczba)``` - wybieramy wielkość generacji, **Alg. ga**
* ```--stagnation_limit (liczba)``` - wybieramy maksymalną liczbę stagnacji, **Alg. ga**
* ```--elite_size (liczba)``` - wybieramy ilość elit, **Alg. ga**
* ```--crossover_method one_point/uniform``` - wybieramy typ krzyżowania, **Alg. ga**
* ```--mutation_method swap/bit_flip``` - wybieramy typ mutacji, **Alg. ga**
* ```--stop_condition stagnation_limit/max_generations``` - wybieramy warunek końca, **Alg. ga**
* ```--suppress 0/1``` - uruchamiamy porównanie bez printów, aby pokazać rzeczywisty czas wykonywania porównywanych algorytmów, **Alg. compare**

## Wybrane algorytmy

* full_enumeration **(enum)**
    * Algorytm pełnego przeglądu (zachłanny) - tworzy tablice kartezjańską, i tworzy wszystkie możliwe opcje załadowacyh przedmiotów do plecaka
* hill_climbing **(hcd i hcr)**
    * Algorytm wspinaczkowy - w wersji deterministycznej wybiera najlepszego sąsiada spośród możliwych o ile jest do wyboru. W wersji losowej wybiera losowego sąsiada i patrzy czy jest lepszy od aktualnego rozwiązania
* tabu_search **(tabu)**
    * Algorytm tabu - Sprawdza możliwych sąsiadów aktualnego rozwiązania i wybiera z nich najlepszego, gdy wybrany sąsiad będzie lepszy on najlepszego wcześniej wybranego zapisuje go jako najlepszy wynik. Zapisuję wszystkie przejścia do listy tabu (o określonej wielkości), i nie pozwala na wybranie sąsiada który znajduje się w liście tabu (o ile nie pozwolimy na cofanie się)
* simulated_annealing **(sa)**
    * Algorytm symulowanego wyżarzania - Rozpoczyna od losowego rozwiązania i w każdej iteracji wybiera losowego sąsiada. Jeśli nowy sąsiad jest lepszy, zostaje zaakceptowany jako nowe rozwiązanie. Gorsze rozwiązania mogą być również zaakceptowane z pewnym prawdopodobieństwem, które zależy od tzw. temperatury – na początku wysokiej, potem malejącej zgodnie z ustalonym harmonogramem chłodzenia. Dzięki temu algorytm może „uciec” z lokalnego optimum, ale z czasem coraz bardziej skupia się na poprawie wyniku.
* genetic_algorithm **(ga)**
    * Algorytm genetyczny – Rozpoczyna od populacji losowych rozwiązań (osobników). W każdej generacji wybierani są rodzice, którzy krzyżują się tworząc nowe rozwiązania. Potomkowie są następnie mutowani. Najlepsze rozwiązania (elity) mogą być bez zmian przenoszone do kolejnej generacji. Proces powtarza się przez ustaloną liczbę pokoleń lub stagnacji pokoleń. Celem jest ewolucyjne polepszanie populacji w kierunku lepszych wyników.
* compare
    * Porównanie - program prównuje wszystkie algorytmy po 5 razy zwracając wykres wartość otrzymaych rozwiązań, oraz analogiczny wykres czasu wykonywania tych algorytmów

## Przykładowe uruchomienie algorytmów
* full_enumeration
    * ```python run_all.py data/input.txt --algorithm enum --max_iteration 1000```
* hill_climbing
    * ```python run_all.py data/input.txt --algorithm hcr --max_iteration 1000```
* tabu_search
    * ```python run_all.py data/input.txt --algorithm tabu --max_iteration 1000 --tabu_size 0 --allow_backtrack 0```
* simulated_annealing
    * ```python run_all.py data/input.txt --algorithm sa --max_iteration 1000 --cooling_schedule linear --alpha 0```
* genetic_algorithm
    * ```python run_all.py data/input.txt --algorithm ga --population_size 25 --max_generations 40 --elite_size 2 --crossover_method one_point --mutation_method swap --stop_condotion max_generations```
* compare
    * ```python run_all.py data/input.txt --algorithm compare --suppress 1```
