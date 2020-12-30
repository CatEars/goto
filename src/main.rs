extern crate term;

mod storage;
use std::cmp::max;
use clap::{App, Arg};
use storage::{ensure_directory_structure, get_current_profile};

fn parse_opts() -> clap::ArgMatches {
    return App::new("Goto")
        .version("2.0")
        .author("Henrik 'CatEars' A. <catears13@gmail.com>")
        .about("Give your terminal teleporting powers")
        .arg(
            Arg::new("add")
                .short('a')
                .long("add")
                .about("Add a new teleport to the current profile")
                .takes_value(true),
        )
        .arg(
            Arg::new("get")
                .short('g')
                .long("get")
                .about("Print a teleport target.")
                .takes_value(true),
        )
        .arg(
            Arg::new("prefix")
                .long("prefix")
                .about("List all targets that have X as prefix")
                .takes_value(true),
        )
        .arg(Arg::new("remove")
             .short('r')
             .long("remove")
             .about("Remove a teleport from the current profile")
             .takes_value(true)
        )
        .arg(
            Arg::new("list")
                .short('l')
                .long("list")
                .about("Lists all teleports")
        )
        .get_matches();
}

/*
Usage: _gotohelper [OPTIONS]

CLI for teleporting to anywhere on your computer!

Options:
-a, --add TEXT        Add a teleport ([name:]path/to/directory)
-g, --get TEXT        Print a teleport target
--prefix TEXT         List all targets that have X as prefix
-r, --remove TEXT     Remove a teleport
-l, --list            List all teleports
-m, --rmprofile TEXT  Remove a profile
-p, --profile TEXT    Switch to a (possibly non-existant) profile
--profiles            List all profiles
--install [bash|zsh]  Install goto for the given shell, "bash" or "zsh"
--help                Show this message and exit.
 */

fn list_profile() {
    let mut t = term::stdout().unwrap();

    let profile = get_current_profile();
    let key_length = profile
        .keys()
        .map(|x| x.len())
        .fold(0, |a, b| max(a, b));

    for k in profile.keys() {
        t.fg(term::color::GREEN).unwrap();
        write!(t, "{:<width$}", k, width = key_length + 1).unwrap();
        t.fg(term::color::WHITE).unwrap();
        write!(t, " -> ").unwrap();
        t.fg(term::color::GREEN).unwrap();
        let x = profile[k].as_str().unwrap();
        writeln!(t, "{}", x).unwrap();
    }

    t.reset().unwrap();
}

fn main() {
    ensure_directory_structure();
    let matches = parse_opts();

    if let Some(x) = matches.value_of("add") {
        println!("Add={}", x);
    } else if let Some(x) = matches.value_of("get") {
        println!("Get={}", x);
    } else if let Some(x) = matches.value_of("prefix") {
        println!("Prefix={}", x);
    } else if let Some(x) = matches.value_of("remove") {
        println!("Remove={}", x);
    } else if matches.occurrences_of("list") == 1 {
        list_profile();
    } else {
        println!("Oh noes, not valid, lol =P");
        panic!("I am the panic");
    }
}
