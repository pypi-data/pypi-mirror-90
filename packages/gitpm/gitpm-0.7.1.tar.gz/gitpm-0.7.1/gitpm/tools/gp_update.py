#! /usr/bin/python3

import argparse, sys, os
from cliprint import color, print_table, table

from ..core import Project


class GitPMUpdate:

    """
    'gitpm update' is a tool to get two projects to have the same progress.
    """

    @staticmethod
    def error(e):
        GitPMUpdate.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm update'.
        """

        GitPMUpdate.parser = argparse.ArgumentParser(
            prog="gitpm update",
            description="Compare and update a project clone with the original.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMUpdate.parser.add_argument(
            "original", help="The project to update (from or to depends)"
        )
        GitPMUpdate.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Display an extensive update log",
        )

        return GitPMUpdate.parser

    @staticmethod
    def format_short(msg, length=16, end="..."):

        """
        Display a message or "..." if it is too long.
        """

        msg = str(msg)
        if len(msg) < length:
            return msg
        else:
            return msg[: length - 3] + end

    @staticmethod
    def isEqual(name, a, b, verbose=False):

        """
        Compare values and pretty-print diff if verbose.
        """

        length = 24
        sign_equals = {
            True: color.f.green + "==" + color.end,
            False: color.f.red + "!=" + color.end,
        }

        equality = a == b
        if not verbose:
            return equality

        print(
            table(
                [16, length + 2, 4, length + 2],
                [
                    [
                        color.f.bold + name + (":" if name else "") + color.end,
                        GitPMUpdate.format_short(a, length),
                        sign_equals[equality],
                        GitPMUpdate.format_short(b, length),
                    ],
                ],
            ),
            end="",
        )

        return equality

    @staticmethod
    def askUpdateMetadata(name, options, projects, set_actions):

        """
        Update Metadata if the user wants to.
        """

        update_input = input("Update " + name + "? (y/n) ").lower()

        if update_input and update_input[0] == "y":
            if options[0] in ["undefined", ""]:
                update_input = "2"
            elif options[1] in ["undefined", ""]:
                update_input = "1"
            else:
                update_input = input(
                    "1: '" + options[0] + "' or\n2: '" + options[1] + "'? (1/2) "
                ).lower()

            if update_input == "1":
                set_actions[1](projects[1], options[0])
            elif update_input == "2":
                set_actions[0](projects[0], options[1])

    # returns 0 if nothing was to be updated, else 1
    @staticmethod
    def updateProjects(project_1, project_2, path=os.getcwd(), verbose=False, end=True):

        """
        Compare and ask to update two projects with oneanother.
        """

        projects = (project_1, project_2)

        if verbose:
            print(
                color.f.bold
                + "Comparing project at '"
                + project_1.path
                + "' and at '"
                + project_2.path
                + "':\n"
                + color.end
            )

        # --- Prepare information
        comparators = ["Name", "Id", "Status", "Description", "Tags", "Log"]
        getters = [
            Project.getName,
            Project.getId,
            Project.getStatus,
            Project.getDescription,
            Project.getTags,
            Project.listCommits,
        ]
        setters = [
            Project.setName,
            Project.setId,
            Project.setStatus,
            Project.setDescription,
            Project.setTags,
            None,
        ]
        values = dict(zip(comparators, [[] for i in range(len(comparators))]))
        comp_getters = dict(zip(comparators, getters))
        comp_setters = dict(zip(comparators, setters))
        equality = dict()

        # --- Get Comparator Data
        for project in projects:
            for comp in comparators:
                values[comp].append(comp_getters[comp](project))

        # --- Compare Data
        for comp in comparators:
            equality[comp] = GitPMUpdate.isEqual(comp, *values[comp], verbose)

        if verbose:
            print()

        # --- End if everything is equal
        if all(equality.values()):
            if end:
                print(color.f.bold + "Equal projects. Nothing to do." + color.end)
            return 0
        elif equality["Log"] and end:
            print(color.f.bold + "Equal commit-logs." + color.end)

        # --- Update changes if unequal commitlogs
        if not equality["Log"]:
            common_hist = [c for c in values["Log"][0] if c in values["Log"][1]]

            if common_hist == []:
                if end:
                    print(
                        color.f.bold + "No common commit history. Aborting." + color.end
                    )
                return 0

            for i in range(2):
                log = values["Log"][i]
                other_log = values["Log"][{1: 0, 0: 1}[i]]
                project = projects[i]
                other_project = projects[{1: 0, 0: 1}[i]]

                if common_hist == log:
                    ahead_project = other_project
                    behind_project = project
                    ahead_amount = len(other_log) - len(common_hist)

            try:  # check if vars were defined
                ahead_project, behind_project, ahead_amount
            except NameError:
                if end:
                    print(
                        color.f.bold
                        + "Weird things happening. Resolve it manually with git."
                        + color.end
                    )
                return 0

            print(
                "Project at '" + ahead_project.path + "' is",
                ahead_amount,
                "commit" + ("" if ahead_amount == 1 else "s") + " ahead.",
            )

            push_input = input("Update? (y/n) ").lower()
            if push_input and push_input[0] == "y":
                if behind_project.type == "repo":
                    behind_project.execute(
                        ["git", "pull", os.path.join(path, ahead_project.path)]
                    )
                else:
                    if ahead_project.type == "bare":
                        ahead_project.execute(
                            [
                                "git",
                                "push",
                                "--set-upstream",
                                os.path.join(path, behind_project.path),
                                ahead_project.getCurrentBranch(),
                            ]
                        )
                    else:
                        ahead_project.execute(
                            ["git", "push", os.path.join(path, behind_project.path)]
                        )

        # --- update metadata if needed
        for comp in comparators:
            if not comp_setters[comp]:  # only modifyable metadata
                continue

            if not equality[comp]:
                GitPMUpdate.askUpdateMetadata(
                    comp,
                    values[comp],
                    projects,
                    [comp_setters[comp] for p in projects],
                )

        return 1

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm update'.
        """

        if args == None:  # parse args using own parser
            GitPMUpdate.generateParser()
            args = GitPMUpdate.parser.parse_args(sys.argv[1:])

        GitPMUpdate.updateProjects(
            Project.fromSelector(args.project),
            Project(args.original),
            path=path,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    GitPMUpdate.main()
