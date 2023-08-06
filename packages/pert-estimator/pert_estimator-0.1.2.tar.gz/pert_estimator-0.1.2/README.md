# Pert Estimator
PERT estimation tool

## Overview

*__NOTE__: The descriptions of the numbers and calculations provided in this section (and frankly the idea for this project) were taken from [The Clean Coder](https://www.amazon.com/Clean-Coder-Conduct-Professional-Programmers/dp/0137081073) by Robert C. Martin*

PERT is an estimating technique which uses three numbers to compute a final estimation (expected duration) and a standard deviation. The three numbers you provide are

- __O__: Optimistic Estimate. This number is wildly optimistic. You could only get the task done this quickly if absolutely everything went right. Indeed, in order for the math to work this number should have much less than a 1% change of occurrence.
- __N__: Nominal Estimate. This is the estimate with the greatest chance of success.
- __P__: Pessimistic Estimate. Once again this is wildly pessimistic. It should include everything except hurricanes, nuclear war, stray black holes, and other catastrophes. Again, the math only works if this number has much less than a 1% change of success.

### Calculations

Expected Duration:

    (O + 4N + P) / 6

_This gives you the final estimation for the task given the 3 estimates provided._

Standard Deviation:

    (P - O) / 6

_This gives you a measure of how uncertain the expected duration is. When this number is large, the uncertainty is large too._

## Usage

From the command line:

    $ pert_estimator
    Task name: test
    Optimistic estimate: .5
    Nominal estimate: 2
    Pessimistic estimate: 6
    Add task? (Y/N): n

    +------+------------+---------+-------------+-------------------+--------------------+
    | Task | Optimistic | Nominal | Pessimistic | Expected Duration | Standard Deviation |
    +------+------------+---------+-------------+-------------------+--------------------+
    | test |    0.5     |    2    |      6      |        2.4        |        0.9         |
    +------+------------+---------+-------------+-------------------+--------------------+
