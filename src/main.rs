extern crate term;

mod storage;
mod embedded;
mod paths;
use clap::{App, Arg};
use std::cmp::max;
use storage::{ensure_directory_structure, get_current_profile};

fn parse_opts() -> clap::App<'static> {
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
        .arg(
            Arg::new("remove")
                .short('r')
                .long("remove")
                .about("Remove a teleport from the current profile")
                .takes_value(true),
        )
        .arg(
            Arg::new("list")
                .short('l')
                .long("list")
                .about("Lists all teleports"),
        )
        .arg(
            Arg::new("install")
                .long("install")
                .about("Installs `goto` function into linux shell."),
        )
        .arg(
            Arg::new("powershell-install")
                .long("powershell-install")
                .about("Installs `goto` function into powershell"),
        )
        .arg(
            Arg::new("config-dir")
                .long("config-dir")
                .about("Prints the directory where goto configuration is stored")
        );

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
--install             Install goto for the given shell, "bash" or "zsh"
--help                Show this message and exit.
 */

fn list_profile() {
    let msg = "Need access to the terminal, but couldn't get that";
    let mut t = term::stdout().expect(msg);

    let profile = get_current_profile().unwrap();
    let max_key_length = profile.keys().map(|x| x.len()).fold(0, |a, b| max(a, b));

    for k in profile.keys() {
        t.fg(term::color::GREEN).unwrap();
        write!(t, "{:<width$}", k, width = max_key_length + 1).unwrap();
        t.fg(term::color::WHITE).unwrap();
        write!(t, " -> ").unwrap();
        t.fg(term::color::GREEN).unwrap();
        let x = profile[k].as_str().unwrap();
        writeln!(t, "{}", x).unwrap();
    }

    t.reset().unwrap();
}

fn get_from_profile(key: &str) {
    let mut t = term::stdout().unwrap();

    let mut real_key = String::from(key);
    if real_key.ends_with("/") {
        real_key.pop();
    }

    let profile = get_current_profile().unwrap();
    let ans = profile.get(&real_key);

    match ans {
        Some(x) => {
            let v = x.as_str().unwrap();
            writeln!(t, "{}", v).unwrap();
        }
        _ => {
            t.fg(term::color::RED).unwrap();
            writeln!(t, "{} is not a valid teleport.", key).unwrap();
            t.reset().unwrap();
        }
    }
}


fn add_teleport_to_profile(teleport_name: &str, directory_name: &str) {
    let term_msg = "Need access to the terminal, but couldn't get that";
    let mut t = term::stdout().expect(term_msg);
    let path = std::path::Path::new(directory_name);

    if !path.is_dir() {
        t.fg(term::color::RED).unwrap();
        writeln!(t, "Could not find {}.", directory_name).unwrap();
        writeln!(t, "Is it really a directory").unwrap();
        t.reset().unwrap();
        return;
    }

    let canonical_path = paths::canonicalize_path(&path.to_path_buf()).display().to_string();
    storage::save_to_current_profile(teleport_name, &canonical_path);

    t.fg(term::color::GREEN).unwrap();
    writeln!(t, "Added '{}' which points to '{}'", teleport_name, canonical_path).unwrap();
    t.reset().unwrap();
}

fn do_remove_from_profile(key: &str) {
    let term_msg = "Need access to the terminal, but couldn't get that";
    let mut t = term::stdout().expect(term_msg);

    if storage::remove_from_profile(key) {
        t.fg(term::color::GREEN).unwrap();
        writeln!(t, "'{}' is no longer a valid teleport", key).unwrap();
    } else {
        t.fg(term::color::RED).unwrap();
        writeln!(t, "'{}' is not a teleport, could not remove", key).unwrap();
    }

    t.reset().unwrap();
}

fn add_to_profile(key: &str) {
    let term_msg = "Need access to the terminal, but couldn't get that";
    let mut t = term::stdout().expect(term_msg);

    let items = key.split(":").collect::<Vec<_>>();
    if items.len() == 1 {
        let telepath = std::path::Path::new(items[0]).to_path_buf();
        let canonical = paths::canonicalize_path(&telepath);
        let fname = canonical.file_name().unwrap();
        let as_str = fname.to_str().unwrap();
       add_teleport_to_profile(as_str, items[0]);
    } else if items.len() == 2 {
        add_teleport_to_profile(items[0], items[1]);
    } else {
        t.fg(term::color::RED).unwrap();
        writeln!(
            t,
            "'{}' is not formatted like expected. Format is 'teleport:directory'",
            key
        )
        .unwrap();
        t.reset().unwrap();
    }
}

fn do_prefix(key: &str) {
    let profile = storage::get_current_profile().unwrap();

    let matches: Vec<String> = profile
        .keys()
        .filter(|x| x.starts_with(key))
        .map(|x| String::from(x))
        .collect();
    if matches.len() == 0 {
        return;
    } else if matches.len() == 1 {
        println!("{}/", matches[0]);
    } else {
        print!("{}/", matches[0]);
        for k in 1..matches.len() {
            print!(" {}/", matches[k]);
        }
        println!("");
    }
}

fn print_source_install() {
    let path = paths::get_config_script_path("goto").display().to_string();
    println!("");
    println!("# add `goto` command to shell");
    println!("if [ -f {} ]; then", path);
    println!("  source {}", path);
    println!("fi");
    println!("");
}

fn print_powershell_source_install() {
    let path = paths::get_config_script_path("goto").display().to_string();
    println!("");
    println!("# goto profile");
    println!("$GotoPath = \"{}\"", path);
    println!("if (Test-Path($GotoPath)) {{");
    println!("  . \"$GotoPath\"");
    println!("}}");
    println!("");
}

fn do_install() {
    storage::install_latest_scripts();
    print_source_install()
}

fn do_powershell_install() {
    storage::install_latest_scripts();
    print_powershell_source_install();
}

fn do_config_dir() {
    let path = paths::get_config_dir().display().to_string();
    println!("{}", path);
}

fn main() {
    ensure_directory_structure();
    let mut app = parse_opts();
    let matches = app.get_matches_mut();

    if let Some(x) = matches.value_of("add") {
        add_to_profile(x);
    } else if let Some(x) = matches.value_of("get") {
        get_from_profile(x);
    } else if let Some(x) = matches.value_of("remove") {
        do_remove_from_profile(x);
    } else if matches.occurrences_of("list") == 1 {
        list_profile();
    } else if let Some(x) = matches.value_of("prefix") {
        do_prefix(x);
    } else if matches.occurrences_of("install") == 1 {
        do_install();
    } else if matches.occurrences_of("powershell-install") == 1 {
        do_powershell_install();
    } else if matches.occurrences_of("config-dir") == 1 {
        do_config_dir();
    } else {
        app.write_help(&mut std::io::stdout()).unwrap();
    }
}
