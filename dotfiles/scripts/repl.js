const repl = require('repl');
const os = require('os');
const chalk = require('chalk');
const exec = require('child_process').exec;
const { promisify } = require('util');

const asyncExec = promisify(exec);

//TODO: Support any language, the base of the shell should be written in C or Rust and bind to Python, Javascript, etc as necessary
//The base language would need to pass any info we don't normally get from the os that we need

//console.log(eval(`'${process.env.PS1.replace('\\u', '\\n')}'`));
async function getPS1(){
    //TODO: So this is nasty...
    //Windows: Considering this can't natively run shell scripts, it would need to reply on msys2 bash
    //Unix: This should be able to run __git_ps1 directly
    //but at the end of the day, we'd rather query git directly or something because running a shell script
    //to get this info defeats the purpose... Can we use isomorphic-git or similar git bindings?
    let gitPS1 = (await asyncExec('bash -l -c __git_ps1')).stdout;
    return `${chalk.green(`${os.userInfo().username}@${os.hostname()}`)} ${chalk.red('JS')} ${chalk.yellow(process.cwd())}${chalk.blue(gitPS1)}
$ `;
}

async function main() {
    repl.start({
        prompt: await getPS1(),
        useColors: true,
        terminal: true,
        eval: async (cmd, context, filename, callback)=>{
            //const func = new Function(`return ${cmd};`);
            let ret, err = null;
            try {
                ret = eval(cmd);
                //No need to print ret, it'll print on callback
            }
            catch(e) {
                err = e;
            }
            repl.repl.setPrompt(await getPS1());
            callback(err, ret);
        }
    });
}
main();