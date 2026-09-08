// C25 separate exhaustive checker: U subsets, D assignments, vertex-simple walks.
// No includes/imports of any other candidate implementation.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#include <openssl/evp.h>
#include <sys/resource.h>
#include <unistd.h>
using namespace std;
void demand(bool b,const char*s){if(!b)throw runtime_error(s);}
int n,m;vector<pair<int,int>> E;vector<vector<pair<int,int>>> adj;
struct Witness {array<int,4> edges;};vector<Witness> obs;set<unsigned> observed;
vector<array<int,2>> touching;array<int,15>w{};array<uint64_t,15> base{};
struct Record{uint64_t code;array<unsigned char,32>cost;int phases;};vector<Record> records;
struct Info{bool valid=false,span=false,perfect=false;int k=0,lmax=0;array<unsigned,32>five{};};vector<Info> infos;
vector<int> D;vector<vector<int>> completed;unsigned umask;uint64_t visits=0;
void walk(int start,int at,unsigned used,vector<int>&path){
 if(path.size()==4)return;
 for(auto [v,e]:adj[at]){
  if(used>>v&1){
   if(v==start&&path.size()==3){unsigned mask=1u<<e;for(int f:path)mask|=1u<<f;
    if(observed.insert(mask).second){Witness a;copy(path.begin(),path.end(),a.edges.begin());a.edges[3]=e;obs.push_back(a);}}
  }else{
   path.push_back(e);
   if(path.size()==4){unsigned mask=0;for(int f:path)mask|=1u<<f;if(observed.insert(mask).second){Witness a;copy(path.begin(),path.end(),a.edges.begin());obs.push_back(a);}}
   else walk(start,v,used|(1u<<v),path);
   path.pop_back();
  }
 }
}
Info decompose(unsigned U){
 Info f;vector<int>degree(n);unsigned unseen=U;vector<vector<int>>paths;unsigned allvertices=0;
 for(int i=0;i<m;++i)if(U>>i&1){++degree[E[i].first];++degree[E[i].second];}
 if(*max_element(degree.begin(),degree.end())>2)return f;
 while(unseen){int seed=__builtin_ctz(unseen);set<int>verts;vector<int>stack{E[seed].first};unsigned component=0;verts.insert(stack[0]);
  while(!stack.empty()){int a=stack.back();stack.pop_back();for(auto [b,e]:adj[a])if(U>>e&1){component|=1u<<e;if(verts.insert(b).second)stack.push_back(b);}}
  int len=__builtin_popcount(component);if(len>3||int(verts.size())!=len+1)return f;
  vector<int>ends;for(int a:verts)if(degree[a]==1)ends.push_back(a);if(ends.size()!=2)return f;
  vector<int>path;int v=ends[0],last=-1;for(int j=0;j<len;++j){int found=-1,next=-1;for(auto [a,e]:adj[v])if((component>>e&1)&&e!=last){found=e;next=a;break;}demand(found>=0,"U order");path.push_back(found);last=found;v=next;}
  paths.push_back(path);for(int a:verts)allvertices|=1u<<a;unseen&=~component;f.lmax=max(f.lmax,len);
 }
 f.k=paths.size();demand(f.k<=5,"phase cap");f.valid=true;f.span=allvertices==(1u<<n)-1;f.perfect=f.span&&__builtin_popcount(U)*2==n;
 for(int s=0;s<(1<<f.k);++s)for(int j=0;j<f.k;++j)for(int p=0;p<int(paths[j].size());++p)if(((s>>j&1)^(p%2))==0)f.five[s]|=1u<<paths[j][p];
 return f;
}
void collect(uint64_t code){
 const Info &f=infos[umask];Record r;r.code=code;r.phases=1<<f.k;r.cost.fill(255);vector<unsigned>pairs;
 for(const auto &a:obs){const auto &es=a.edges;int zeros=0;for(int i=0;i<4;++i)if(!w[es[i]])zeros|=1<<i;
  if(zeros==5&&w[es[1]]==w[es[3]])pairs.push_back((1u<<es[0])|(1u<<es[2]));
  if(zeros==10&&w[es[0]]==w[es[2]])pairs.push_back((1u<<es[1])|(1u<<es[3]));
 }
 for(int s=0;s<r.phases;++s){int count=0;for(unsigned pair:pairs){unsigned a=pair&f.five[s];count+=(a==0||a==pair);}demand(count<255,"cost byte");r.cost[s]=count;}
 records.push_back(r);
}
void color(int j,int q,uint64_t code){
 ++visits;if(j==int(D.size())){collect(code);return;}
 int e=D[j];auto [a,b]=E[e];unsigned banned=0;for(int v:{a,b})for(auto [u,f]:adj[v])if(f<e&&w[f])banned|=1u<<w[f];
 for(int c=1;c<=min(4,q+1);++c){if(banned>>c&1)continue;w[e]=c;bool ok=true;
  for(int h:completed[e]){auto es=obs[h].edges;if(w[es[0]]==w[es[2]]&&w[es[1]]==w[es[3]]){ok=false;break;}}
  if(ok)color(j+1,max(q,c),code+c*base[e]);
 }w[e]=0;
}
int main(){try{
 alarm(35);rlimit cpu{30,31},mem{805306368,805306368};setrlimit(RLIMIT_CPU,&cpu);setrlimit(RLIMIT_AS,&mem);
 demand(bool(cin>>n>>m)&&n>=1&&n<=10&&m>=0&&m<=15,"input size");adj.resize(n);set<pair<int,int>>edges;
 for(int e=0;e<m;++e){int a,b;demand(bool(cin>>a>>b)&&0<=a&&a<b&&b<n,"edge");demand(edges.insert({a,b}).second,"duplicate");E.emplace_back(a,b);adj[a].push_back({b,e});adj[b].push_back({a,e});}
 for(const auto&v:adj)demand(v.size()<=3,"degree");vector<int>path;for(int s=0;s<n;++s)walk(s,s,1u<<s,path);
 uint64_t p=1;for(int e=m-1;e>=0;--e){base[e]=p;p*=5;}
 infos.resize(1<<m);records.reserve(1500000);
 for(umask=0;umask<(1u<<m);++umask){infos[umask]=decompose(umask);if(!infos[umask].valid)continue;D.clear();completed.assign(m,{});
  for(int e=0;e<m;++e)if(!(umask>>e&1))D.push_back(e);
  for(int h=0;h<int(obs.size());++h){unsigned mask=0;int last=0;for(int e:obs[h].edges){mask|=1u<<e;last=max(last,e);}if(!(mask&umask))completed[last].push_back(h);}
  color(0,0,0);
 }
 sort(records.begin(),records.end(),[](auto&a,auto&b){return a.code<b.code;});
 struct Stat{uint64_t total=0,balanced=0,word=0;int phase=-1,minimum=255;};vector<Stat>uinfo(1<<m);array<uint64_t,256>hist{};uint64_t raw=0,phases=0,rawphases=0,good=0,short2=0,perfect=0;
 EVP_MD_CTX*ctx=EVP_MD_CTX_new();EVP_DigestInit_ex(ctx,EVP_sha256(),nullptr);string hex="0123456789abcdef";uint64_t previous=0;bool have=false;
 for(auto&r:records){demand(!have||r.code>previous,"unique states");previous=r.code;have=true;unsigned U=0;int q=0;for(int e=0;e<m;++e){int c=r.code/base[e]%5;if(c==0)U|=1u<<e;else q=max(q,c);}
  const Info&f=infos[U];demand(r.phases==(1<<f.k),"phase domain");int best=255,bp=-1;string line=to_string(r.code)+":";
  for(int s=0;s<r.phases;++s){int c=r.cost[s];if(c<best){best=c;bp=s;}line+=hex[c>>4];line+=hex[c&15];}line+='\n';EVP_DigestUpdate(ctx,line.data(),line.size());
  uint64_t orbit=1;for(int i=0;i<q;++i)orbit*=4-i;raw+=orbit;phases+=r.phases;rawphases+=orbit*r.phases;++hist[best];Stat&z=uinfo[U];++z.total;z.minimum=min(z.minimum,best);
  if(!best){++good;++z.balanced;if(z.phase<0){z.word=r.code;z.phase=bp;}short2+=f.span&&f.lmax<=2;perfect+=f.perfect;}
 }
 unsigned char bytes[32];unsigned len;EVP_DigestFinal_ex(ctx,bytes,&len);EVP_MD_CTX_free(ctx);string digest;for(int i=0;i<32;++i){digest+=hex[bytes[i]>>4];digest+=hex[bytes[i]&15];}
 cout<<"{\"verdict\":\"candidate_only\",\"engine\":\"U-subset-direct-witness\",\"n\":"<<n<<",\"m\":"<<m<<",\"frames\":"<<records.size()<<",\"raw_frames\":"<<raw<<",\"phases\":"<<phases<<",\"raw_phases\":"<<rawphases<<",\"balanced\":"<<good<<",\"balanced_spanning_short2\":"<<short2<<",\"balanced_perfect_U\":"<<perfect<<",\"nodes\":"<<visits<<",\"shape_count\":"<<obs.size()<<",\"stream_sha256\":\""<<digest<<"\",\"mu_histogram\":{";
 bool comma=false;for(int i=0;i<256;++i)if(hist[i]){if(comma)cout<<',';cout<<'\"'<<i<<"\":"<<hist[i];comma=true;}cout<<"},\"U_rows\":[";comma=false;
 for(unsigned u=0;u<(1u<<m);++u)if(infos[u].valid){auto&z=uinfo[u];if(comma)cout<<',';comma=true;cout<<'['<<u<<','<<z.total<<','<<z.balanced<<','<<(z.total?z.minimum:-1)<<','<<z.word<<','<<z.phase<<']';}cout<<"]}\n";
 }catch(const exception&e){cerr<<e.what()<<'\n';return 2;}}
