// C25 labelled cubic generation and exact isomorphism coverage. Candidate only.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <vector>
#include <sys/resource.h>
#include <unistd.h>
using namespace std;
int n; using G=array<unsigned,10>;
G a{}; vector<G> reps; vector<uint64_t> counts; uint64_t leaves=0,connected=0;
map<vector<int>, vector<int>> buckets;
vector<int> signature(const G& g){
 vector<int> s;
 for(int v=0;v<n;++v){int t=0,c4=0;
  for(int u=0;u<n;++u)if(g[v]>>u&1)t+=__builtin_popcount(g[v]&g[u]);
  for(int u=0;u<n;++u)if(u!=v){int k=__builtin_popcount(g[v]&g[u]);c4+=k*(k-1)/2;}
  s.push_back(100*t+c4);
 }
 sort(s.begin(),s.end());return s;
}
uint64_t mappings(const G& g,const G& h,bool first){
 array<int,10> f;f.fill(-1);uint64_t answer=0;
 auto dfs=[&](auto&& self,int k,unsigned used)->bool{
  if(k==n){++answer;return first;}
  int v=-1,best=-1;for(int z=0;z<n;++z)if(f[z]<0){int c=0;for(int j=0;j<n;++j)if(f[j]>=0&&(g[z]>>j&1))++c;if(c>best){best=c;v=z;}}
  for(int w=0;w<n;++w)if(!(used>>w&1)){
   bool ok=true;for(int j=0;j<n;++j)if(f[j]>=0&&((g[v]>>j&1)!=(h[w]>>f[j]&1))){ok=false;break;}
   if(!ok){continue;}
   f[v]=w; if(self(self,k+1,used|(1u<<w))){return true;} f[v]=-1;
  }return false;
 };dfs(dfs,0,0);return answer;
}
void complete(){
 ++leaves;unsigned seen=1,old=0;while(seen!=old){old=seen;for(int v=0;v<n;++v)if(seen>>v&1)seen|=a[v];}
 if(seen!=(1u<<n)-1){return;}
 ++connected;
 auto key=signature(a);auto &ids=buckets[key];
 for(int i:ids)if(mappings(a,reps[i],true)){++counts[i];return;}
 ids.push_back(reps.size());reps.push_back(a);counts.push_back(1);
}
void vertices(int v){
 if(v==n){complete();return;}
 int need=3-__builtin_popcount(a[v]);if(need<0)return;
 vector<int> allowed;for(int u=v+1;u<n;++u)if(__builtin_popcount(a[u])<3)allowed.push_back(u);
 auto choose=[&](auto&& self,int p,int k)->void{
  if(!k){
   // All unresolved degree deficits must be fillable by later vertices.
   for(int u=v+1;u<n;++u){int possible=0;for(int w=v+1;w<n;++w)if(w!=u&&!(a[u]>>w&1)&&__builtin_popcount(a[w])<3)++possible;
    if(3-__builtin_popcount(a[u])>possible)return;}
   vertices(v+1);return;
  }
  if(int(allowed.size())-p<k)return;
  for(int j=p;j<=int(allowed.size())-k;++j){int u=allowed[j];a[v]|=1u<<u;a[u]|=1u<<v;self(self,j+1,k-1);a[v]^=1u<<u;a[u]^=1u<<v;}
 };choose(choose,0,need);
}
int main(int argc,char**argv){
 alarm(35);rlimit cpu{30,31},mem{805306368,805306368};setrlimit(RLIMIT_CPU,&cpu);setrlimit(RLIMIT_AS,&mem);
 n=argc>1?atoi(argv[1]):10;if(n<4||n>10||n%2)return 2;
 for(int v=1;v<=3;++v){a[0]|=1u<<v;a[v]|=1;}
 vertices(1);uint64_t fact=1;for(int k=2;k<=n;++k)fact*=k;uint64_t scale=(n-1)*(n-2)*(n-3)/6,sum=0;
 cout<<"{\"verdict\":\"candidate_only\",\"n\":"<<n<<",\"fixed_neighbors\":[1,2,3],\"fixed_neighbor_completions\":"<<leaves<<",\"connected_fixed_neighbor_completions\":"<<connected<<",\"label_multiplier\":"<<scale<<",\"graphs\":[";
 for(size_t i=0;i<reps.size();++i){uint64_t aut=mappings(reps[i],reps[i],false);assert(aut&&fact%aut==0);assert(fact/aut==counts[i]*scale);sum+=fact/aut;
  if(i){cout<<',';}
  cout<<"{\"index\":"<<i<<",\"automorphisms\":"<<aut<<",\"labelled_count\":"<<fact/aut<<",\"fixed_neighbor_count\":"<<counts[i]<<",\"edges\":[";bool comma=false;
  for(int v=0;v<n;++v)for(int u=v+1;u<n;++u)if(reps[i][v]>>u&1){if(comma)cout<<',';cout<<'['<<v<<','<<u<<']';comma=true;}
  cout<<"]}";
 }
 assert(sum==connected*scale);cout<<"],\"types\":"<<reps.size()<<",\"connected_labelled_total\":"<<sum<<"}\n";
}
