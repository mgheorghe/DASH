# SONiC DASH
## Governance

## Goals
The goal of governance for the project is to maintain and emphasize a technical meritocracy of contributors.  Those
who contribute the most and the best technical solutions, have the most influence in the direction of the project.
An element of benevolent dictatorship exists per component and at an overall project level to keep the project
successful and resolve conflict.

## Structure
The project consists of many repositories that will change over time as the project evolves. Each repository is
expected to be self governing with a maintainer leading it.

A key repository in the project is MAIN.  TBD build-repo is the authoritative list of all the necessary source
code repositories needed to create the official distribution of the project.

## Roles and responsibilities
- *Contributors* are people who have submitted work to the project.  Work includes all kinds of tasking, including
things like code, tests, code reviews, documentation, infrastructure and proposals.
- *Maintainers* have permission to accept pull requests and merge them into the master branch of a given repository.
Each repository contains a MAINTAINERS file listing the maintainers.  There must be one or more named maintainers
per repository.
- The *Project Leader* is responsible for the success of the project and resolving conflict between the maintainers
and keep the project.  Today the project leader is appointed by Microsoft.  A new Project Leader is expected to be
appointed by the Open Compute Project when it is accepted.

## Conflict Resolution
Each repository is expected to resolve conflicts for itself and between dependent repositories.  If a resolution
cannot be found in a reasonable time, the issue will be escalated to the Project Leader who will help the teams
find a solution to move the project forward.

### Example of conflict resolution
If a repository merge change is is incompatible with the other parts of a project, for example.
At a minimum, the build-repo maintainer will detect this and continue to build with the older
release of the repo(s) under issue.  The community discusses the changes.

Updates to the project emerge requiring a change.  The community has not achieved consensus on the earlier
change and moving on to a new build is now blocked.  The project leader will step in to arbitrate and reach
a decision that will unblock the build and with the greatest technical merit.
