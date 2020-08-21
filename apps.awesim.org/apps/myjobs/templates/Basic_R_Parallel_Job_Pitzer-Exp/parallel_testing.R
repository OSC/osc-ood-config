myProc <- function(size=100000000) {
  # Load a large vector
  vec <- rnorm(size)
  # Now sum the vec values
  return(sum(vec))
}
 
detachDoParallel <- function() {
  detach("package:doParallel")
  detach("package:foreach")
  detach("package:parallel")
  detach("package:iterators")
}
 
max_loop <- 100
 
# version 1: use mclapply (multicore) - warning - generates zombie processes
library(parallel)
 
tick <- proc.time()
result <- mclapply(1:max_loop, function(i) myProc(), mc.cores=detectCores())
tock <- proc.time() - tick
 
cat("\nmclapply/multicore test times using", detectCores(), "cores: \n")
tock
 
# version 2: use foreach with explicit MPI cluster on one node
library(doParallel, quiet = TRUE)
library(Rmpi)
 
slaves <- detectCores() - 1
{ sink("/dev/null"); cl_onenode <- makeCluster(slaves, type="MPI"); sink(); } # number of MPI tasks to use
registerDoParallel(cl_onenode)
 
tick <- proc.time()
result <- foreach(i=1:max_loop, .combine=c) %dopar% {
    myProc()
}
tock <- proc.time() - tick
 
cat("\nforeach w/ Rmpi test times using", slaves, "MPI slaves: \n")
tock
 
invisible(stopCluster(cl_onenode))
detachDoParallel()
 
# version 3: use foreach (multicore)
library(doParallel, quiet=TRUE)
 
cores <- detectCores()
cl <- makeCluster(cores)
registerDoParallel(cl)
 
tick <- proc.time()
result <- foreach(i=1:max_loop, .combine=c) %dopar% {
    myProc()
}
tock <- proc.time() - tick
 
cat("\nforeach w/ fork times using", cores, "cores: \n")
tock
 
invisible(stopCluster(cl))
detachDoParallel()
 
## version 4: use foreach (doSNOW/Rmpi)
library(doParallel, quiet = TRUE)
library(Rmpi)
 
slaves <- as.numeric(Sys.getenv(c("PBS_NP")))-1
{ sink("/dev/null"); cl <- makeCluster(slaves, type="MPI"); sink(); } # number of MPI tasks to use
registerDoParallel(cl)
 
tick <- proc.time()
result <- foreach(i=1:max_loop, .combine=c) %dopar% {
    myProc()
}
tock <- proc.time() - tick
 
cat("\nforeach w/ Rmpi test times using", slaves, "MPI slaves: \n")
tock
 
detachDoParallel() # no need to stop cluster we will use it again
 
## version 5: use snow backed by Rmpi (cluster already created)
library(Rmpi) # for mpi.*
library(snow) # for clusterExport, clusterApply
 
#slaves <- as.numeric(Sys.getenv(c("PBS_NP")))-1
clusterExport(cl, list('myProc'))
 
tick <- proc.time()
result <- clusterApply(cl, 1:max_loop, function(i) myProc())
tock <- proc.time() - tick
 
cat("\nsnow w/ Rmpi test times using", slaves, "MPI slaves: \n")
tock
 
invisible(stopCluster(cl))
mpi.quit()