'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const path = require("path");
const tkill = require("tree-kill");
const component = require("../../../common/component");
const experimentStartupInfo_1 = require("../../../common/experimentStartupInfo");
const log_1 = require("../../../common/log");
const trialConfigMetadataKey_1 = require("../../common/trialConfigMetadataKey");
const environment_1 = require("../environment");
const utils_1 = require("../../../common/utils");
const util_1 = require("../../common/util");
let LocalEnvironmentService = class LocalEnvironmentService extends environment_1.EnvironmentService {
    constructor() {
        super();
        this.log = log_1.getLogger();
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.experimentRootDir = utils_1.getExperimentRootDir();
    }
    get environmentMaintenceLoopInterval() {
        return 100;
    }
    get hasStorageService() {
        return false;
    }
    get getName() {
        return 'local';
    }
    async config(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                this.localTrialConfig = JSON.parse(value);
                break;
            default:
                this.log.debug(`Local mode does not proccess metadata key: '${key}', value: '${value}'`);
        }
    }
    async refreshEnvironmentsStatus(environments) {
        environments.forEach(async (environment) => {
            const jobpidPath = `${environment.runnerWorkingFolder}/pid`;
            const runnerReturnCodeFilePath = `${environment.runnerWorkingFolder}/code`;
            try {
                const pidExist = await fs.existsSync(jobpidPath);
                if (!pidExist) {
                    return;
                }
                const pid = await fs.promises.readFile(jobpidPath, 'utf8');
                const alive = await utils_1.isAlive(pid);
                environment.status = 'RUNNING';
                if (!alive) {
                    if (fs.existsSync(runnerReturnCodeFilePath)) {
                        const runnerReturnCode = await fs.promises.readFile(runnerReturnCodeFilePath, 'utf8');
                        const match = runnerReturnCode.trim()
                            .match(/^-?(\d+)\s+(\d+)$/);
                        if (match !== null) {
                            const { 1: code } = match;
                            if (parseInt(code, 10) === 0) {
                                environment.setStatus('SUCCEEDED');
                            }
                            else {
                                environment.setStatus('FAILED');
                            }
                        }
                    }
                }
            }
            catch (error) {
                this.log.error(`Update job status exception, error is ${error.message}`);
            }
        });
    }
    async startEnvironment(environment) {
        if (this.localTrialConfig === undefined) {
            throw new Error('Local trial config is not initialized');
        }
        const localTempFolder = path.join(this.experimentRootDir, this.experimentId, "environment-temp", "envs");
        const localEnvCodeFolder = path.join(this.experimentRootDir, "envs");
        environment.runnerWorkingFolder = path.join(localEnvCodeFolder, environment.id);
        await util_1.execMkdir(environment.runnerWorkingFolder);
        await util_1.execCopydir(localTempFolder, localEnvCodeFolder);
        environment.command = `cd ${this.experimentRootDir} && \
${environment.command} --job_pid_file ${environment.runnerWorkingFolder}/pid \
1>${environment.runnerWorkingFolder}/trialrunner_stdout 2>${environment.runnerWorkingFolder}/trialrunner_stderr \
&& echo $? \`date +%s%3N\` >${environment.runnerWorkingFolder}/code`;
        await fs.promises.writeFile(path.join(localEnvCodeFolder, 'nni_run.sh'), environment.command, { encoding: 'utf8', mode: 0o777 }),
            util_1.runScript(path.join(localEnvCodeFolder, 'nni_run.sh'));
        environment.trackingUrl = `${environment.runnerWorkingFolder}`;
    }
    async stopEnvironment(environment) {
        const jobpidPath = `${environment.runnerWorkingFolder}/pid`;
        const pid = await fs.promises.readFile(jobpidPath, 'utf8');
        tkill(Number(pid), 'SIGKILL');
    }
};
LocalEnvironmentService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], LocalEnvironmentService);
exports.LocalEnvironmentService = LocalEnvironmentService;
